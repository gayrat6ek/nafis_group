from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserLocationBase(BaseModel):
    location_name: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    apartment_suite: Optional[str] = None
    building_name: Optional[str] = None
    floor_number: Optional[str] = None
    is_default: Optional[bool] = False
    is_active: Optional[bool] = True

class UserLocationCreate(UserLocationBase):
    user_id: Optional[UUID] = None

class UserLocationUpdate(UserLocationBase):
    pass

class UserLocationInDB(UserLocationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserLocation(UserLocationInDB):
    pass
