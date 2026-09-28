"""
Student ORM Model
-----------------
Represents university students who receive parcels at the campus mailroom.

Key Concepts:
- Primary Key (`id`): An internal surrogate key (integer auto-increment).
- Candidate Key (`matric_number`): The student's official university ID (e.g. 'A21EC0045').
  It is marked `unique=True` and `index=True` for instant lookup when mailroom staff search by ID.
- Candidate Key (`email`): Also unique, used for pickup notifications.
- Relationship (`parcels`): Enables reverse lookup `student.parcels` to see all parcels belonging to this student.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    # Internal Primary Key (surrogate key)
    id = Column(Integer, primary_key=True, index=True)

    # University Matriculation / Student ID (e.g. S12345 or A22EC0100)
    # Marked unique so no two students can share the same matric ID.
    matric_number = Column(String(20), unique=True, index=True, nullable=False)

    # Student full name
    name = Column(String(100), nullable=False)

    # Student university email address for pickup notifications
    email = Column(String(120), unique=True, index=True, nullable=False)

    # Optional contact number for SMS or WhatsApp notifications
    phone_number = Column(String(20), nullable=True)

    # Campus accommodation location (e.g. 'College 9, Block B-302')
    dorm_block = Column(String(50), nullable=True)

    # Audit timestamp: automatically records when the student record was created
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # ORM Relationship: One Student has Many Parcels (1-to-N)
    # `back_populates="student"` links this with `Parcel.student`
    parcels = relationship(
        "Parcel",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Student(id={self.id}, matric='{self.matric_number}', name='{self.name}')>"
