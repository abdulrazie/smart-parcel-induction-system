"""
Database Models Package
-----------------------
Exports all ORM models and Base class.
Importing all models here ensures they are registered with SQLAlchemy's metadata
when `Base.metadata.create_all()` is executed.
"""

from app.database import Base
from app.models.student import Student
from app.models.courier import Courier
from app.models.parcel import Parcel, ParcelStatus

__all__ = [
    "Base",
    "Student",
    "Courier",
    "Parcel",
    "ParcelStatus",
]
