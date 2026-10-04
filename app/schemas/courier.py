"""
Courier Pydantic Schemas
------------------------
Defines request and response data contracts for Courier entities.

Key Concepts:
- Normalization reflection: Couriers are represented as a distinct entity in the DB,
  and this schema serializes those records cleanly for API consumers.
- Computed fields: Maps `id` to `courier_id` and `name` to `company_name` to support
  both standard REST naming and project-specific requirements.
"""

from pydantic import BaseModel, ConfigDict, Field, computed_field


class CourierBase(BaseModel):
    """Shared attributes for courier delivery companies."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Courier brand name (e.g. DHL Express, PosLaju, FedEx)"
    )
    is_active: bool = Field(
        default=True,
        description="Whether this courier is actively accepted at the mailroom"
    )


class CourierResponse(CourierBase):
    """
    Schema for returning courier details in API responses.
    Reads directly from SQLAlchemy `Courier` ORM instances.
    """
    id: int = Field(..., description="Internal primary key in the database")

    @computed_field
    def courier_id(self) -> int:
        """Alias for `id` providing semantic clarity for consumers."""
        return self.id

    @computed_field
    def company_name(self) -> str:
        """Alias for `name` conforming to university project requirements."""
        return self.name

    model_config = ConfigDict(from_attributes=True)
