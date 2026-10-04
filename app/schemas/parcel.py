"""
Parcel Pydantic Schemas
-----------------------
Defines request and response contracts for parcel intake, queries, and verification.

Key Concepts:
- Input validation: Guarantees incoming payloads adhere to relational rules before
  hitting SQLAlchemy queries (e.g. verifying tracking numbers are non-empty).
- Conditional validation: A model validator ensures at least one identifier
  (`student_matric` or `student_id`) is provided during intake.
- Nested serialization: `ParcelResponse` serializes related `student` and `courier`
  ORM models via SQLAlchemy relationships, mirroring foreign key joins in JSON.
"""

from datetime import datetime
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
    computed_field
)
from app.models.parcel import ParcelStatus
from app.schemas.student import StudentResponse
from app.schemas.courier import CourierResponse


class ParcelIntakeRequest(BaseModel):
    """
    Payload sent by mailroom staff when scanning/logging an incoming parcel.
    Supports either student_matric (counter scan) or direct student_id.
    """
    tracking_number: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Courier tracking barcode/number scanned at intake"
    )
    student_matric: str | None = Field(
        None,
        max_length=20,
        description="Student matric number (e.g. A21EC0001) used to look up student"
    )
    student_id: int | None = Field(
        None,
        description="Direct student database ID (used if known)"
    )
    courier_id: int = Field(
        ...,
        description="ID of the courier company that delivered the package"
    )
    shelf_location: str | None = Field(
        None,
        max_length=30,
        description="Optional manual shelf override. If omitted, assigned temporary induction hold"
    )

    @field_validator("tracking_number")
    @classmethod
    def clean_tracking_number(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Tracking number cannot be empty or blank whitespace.")
        return cleaned

    @field_validator("student_matric")
    @classmethod
    def clean_student_matric(cls, v: str | None) -> str | None:
        if v is not None:
            cleaned = v.strip().upper()
            return cleaned if cleaned else None
        return None

    @model_validator(mode="after")
    def check_student_identifier_provided(self) -> "ParcelIntakeRequest":
        if not self.student_matric and self.student_id is None:
            raise ValueError(
                "Either 'student_matric' or 'student_id' must be provided to associate the parcel."
            )
        return self


class ParcelResponse(BaseModel):
    """
    Full parcel response returned to API consumers.
    Includes nested student and courier details populated from ORM relationships.
    """
    id: int = Field(..., description="Internal parcel primary key")
    tracking_number: str = Field(..., description="Unique carrier tracking number")
    student_id: int = Field(..., description="Foreign key reference to students.id")
    courier_id: int = Field(..., description="Foreign key reference to couriers.id")
    shelf_location: str = Field(..., description="Physical shelf location in the mailroom")
    status: ParcelStatus = Field(..., description="Current lifecycle state (pending, picked_up, returned)")
    pickup_code: str = Field(..., description="Unique 6-char claim token (e.g. PK-7K8M92)")
    logged_at: datetime = Field(..., description="Timestamp when staff logged the parcel")
    picked_up_at: datetime | None = Field(None, description="Timestamp when parcel was collected")

    # Nested ORM relationships (loaded via SQLAlchemy back_populates)
    student: StudentResponse = Field(..., description="Student recipient information")
    courier: CourierResponse = Field(..., description="Courier delivery details")

    @computed_field
    def parcel_id(self) -> int:
        """Alias for `id` providing semantic clarity for consumers."""
        return self.id

    model_config = ConfigDict(from_attributes=True)


class ParcelVerifyRequest(BaseModel):
    """
    Payload sent by mailroom staff at pickup counter to verify student collection.
    """
    pickup_code: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Unique verification claim code presented by student (e.g. PK-829104)"
    )

    @field_validator("pickup_code")
    @classmethod
    def clean_pickup_code(cls, v: str) -> str:
        cleaned = v.strip().upper()
        if not cleaned:
            raise ValueError("Pickup code cannot be blank.")
        return cleaned


class ParcelVerifyResponse(BaseModel):
    """
    Response returned upon successful pickup verification and handover.
    """
    message: str = Field(..., description="Success confirmation message")
    parcel: ParcelResponse = Field(..., description="Updated parcel record with picked_up_at timestamp")
