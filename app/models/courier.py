"""
Courier ORM Model
-----------------
Represents delivery companies delivering packages to the mailroom (e.g. DHL, FedEx, PosLaju).

Key Concepts:
- Normalization (3NF): By separating couriers into their own table rather than storing raw text
  strings like "DHL" in the parcels table, we eliminate typos (e.g. "DHL" vs "dhl" vs "DHL Express")
  and make it easy to generate statistics per courier.
- Soft toggle (`is_active`): Instead of deleting a courier that is no longer partnered, we can deactivate it.
  This preserves historical parcel data integrity.
"""

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Courier(Base):
    __tablename__ = "couriers"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Courier name (e.g., "DHL Express", "FedEx", "J&T Express", "PosLaju")
    # Unique constraint ensures no duplicate companies can be created.
    name = Column(String(50), unique=True, index=True, nullable=False)

    # Active status: allows disabling inactive couriers from dropdown selections
    is_active = Column(Boolean, default=True, nullable=False)

    # ORM Relationship: One Courier has Many Parcels (1-to-N)
    parcels = relationship(
        "Parcel",
        back_populates="courier"
    )

    def __repr__(self) -> str:
        return f"<Courier(id={self.id}, name='{self.name}', is_active={self.is_active})>"
