"""
Parcel ORM Model
----------------
Represents physical packages checked in at the mailroom.

Key Concepts:
- Foreign Keys (`student_id`, `courier_id`): Enforces referential integrity.
  A parcel cannot exist without a valid student and a valid courier in the database.
- Unique Constraints:
  1. `tracking_number`: A courier tracking number is unique per parcel.
  2. `pickup_code`: A secure verification code (e.g., 'PK-829104') generated when logged.
     This code is embedded into the QR code sent to the student.
- Status Enum (`ParcelStatus`): Prevents invalid statuses and string typos.
- Timestamps:
  1. `logged_at`: When the mailroom staff scanned and assigned the shelf.
  2. `picked_up_at`: When the student presented their pickup code and collected it.
"""

import enum
import secrets
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class ParcelStatus(str, enum.Enum):
    """
    Allowed lifecycle states for a parcel in the mailroom.
    Inheriting from `str` allows smooth serialization to JSON without custom encoders.
    """
    PENDING = "pending"          # In mailroom, awaiting student pickup
    PICKED_UP = "picked_up"      # Collected by the student
    RETURNED = "returned"        # Returned to courier (unclaimed after deadline)


def generate_pickup_code() -> str:
    """
    Generates a human-friendly and QR-scannable claim code.
    Format: 'PK-' followed by 6 random alphanumeric characters (e.g. 'PK-7K8M92').
    """
    token = secrets.token_hex(3).upper()  # 6 characters
    return f"PK-{token}"


class Parcel(Base):
    __tablename__ = "parcels"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Courier Tracking Number (e.g. '1Z9999999999999999' or 'MY123456789')
    # Unique and indexed for rapid scanning / barcode searches.
    tracking_number = Column(String(100), unique=True, index=True, nullable=False)

    # Foreign Key linking to `students.id`
    student_id = Column(Integer, ForeignKey("students.id", ondelete="RESTRICT"), nullable=False, index=True)

    # Foreign Key linking to `couriers.id`
    courier_id = Column(Integer, ForeignKey("couriers.id", ondelete="RESTRICT"), nullable=False, index=True)

    # Physical mailroom storage location (e.g. "Shelf A-02-04" or "Oversized-Bay 3")
    # Indexed so staff can easily view all packages on a specific shelf.
    shelf_location = Column(String(30), nullable=False, index=True)

    # Current lifecycle state
    status = Column(
        SQLEnum(ParcelStatus, name="parcel_status_enum", native_enum=False),
        default=ParcelStatus.PENDING,
        nullable=False,
        index=True
    )

    # Unique claim verification code for QR generation and student validation
    pickup_code = Column(
        String(20),
        default=generate_pickup_code,
        unique=True,
        index=True,
        nullable=False
    )

    # Timestamp when mailroom staff inducted the package
    logged_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Timestamp when student completed pickup (null while pending)
    picked_up_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # ORM Relationships
    student = relationship("Student", back_populates="parcels")
    courier = relationship("Courier", back_populates="parcels")

    def __repr__(self) -> str:
        return (
            f"<Parcel(id={self.id}, tracking='{self.tracking_number}', "
            f"shelf='{self.shelf_location}', status='{self.status}')>"
        )
