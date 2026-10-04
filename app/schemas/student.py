"""
Student Pydantic Schemas
------------------------
Defines request and response data contracts for Student records.

Key Concepts:
- BaseModel: Core Pydantic class providing type validation and serialization.
- ConfigDict(from_attributes=True): Enables Pydantic v2 to read data directly from
  SQLAlchemy ORM models (previously known as `orm_mode=True` in Pydantic v1).
- Computed fields: Adds convenient alias keys like `student_id` matching requirements
  while keeping the internal primary key `id` intact.
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, computed_field


class StudentBase(BaseModel):
    """Shared student attributes used across schemas."""
    matric_number: str = Field(
        ...,
        min_length=2,
        max_length=20,
        description="Official university matriculation/student number (e.g. A21EC0001)"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Full name of the student"
    )
    email: str = Field(
        ...,
        max_length=120,
        description="Official student university email address"
    )
    phone_number: str | None = Field(
        None,
        max_length=20,
        description="Optional contact number for notifications"
    )
    dorm_block: str | None = Field(
        None,
        max_length=50,
        description="On-campus accommodation block/room (e.g. Kolej Rahman, Block A-201)"
    )


class StudentResponse(StudentBase):
    """
    Schema for serializing student information in API responses.
    Reads directly from SQLAlchemy `Student` ORM instances.
    """
    id: int = Field(..., description="Internal primary key in the database")
    created_at: datetime = Field(..., description="Timestamp when the student was registered")

    @computed_field
    def student_id(self) -> int:
        """Alias for `id` providing semantic clarity for consumers."""
        return self.id

    model_config = ConfigDict(from_attributes=True)
