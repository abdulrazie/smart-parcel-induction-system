"""
Pydantic Schemas Package
------------------------
Exports all request and response validation schemas for API routers.
"""

from app.schemas.student import StudentBase, StudentResponse
from app.schemas.courier import CourierBase, CourierResponse
from app.schemas.parcel import (
    ParcelIntakeRequest,
    ParcelResponse,
    ParcelVerifyRequest,
    ParcelVerifyResponse,
)

__all__ = [
    "StudentBase",
    "StudentResponse",
    "CourierBase",
    "CourierResponse",
    "ParcelIntakeRequest",
    "ParcelResponse",
    "ParcelVerifyRequest",
    "ParcelVerifyResponse",
]
