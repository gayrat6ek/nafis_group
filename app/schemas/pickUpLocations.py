
from datetime import datetime
from enum import Enum
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

class PickUpLocationGet(BaseConfig):
    id: Optional[UUID] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    address: Optional[str] = None  # Address of the pickup location
    is_active: Optional[bool] = True  # Indicates if the pickup location is active
    lat: Optional[float] = None  # Latitude for the pickup location
    lon: Optional[float] = None  # Longitude for the pickup location
    created_at: Optional[datetime] = None  # Timestamp when the pickup location was created
    updated_at: Optional[datetime] = None  # Timestamp when the pickup location was last updated


class PickUpLocationList(BaseConfig):
    id: UUID
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    address: Optional[str] = None  # Address of the pickup location
    is_active: Optional[bool] = True  # Indicates if the pickup location is active
    lat: Optional[float] = None  # Latitude for the pickup location
    lon: Optional[float] = None  # Longitude for the pickup location


class PickUpLocationCreate(BaseConfig):
    name_uz: str = Field(..., description="Name of the pickup location in Uzbek")
    name_ru: str = Field(..., description="Name of the pickup location in Russian")
    name_en: str = Field(..., description="Name of the pickup location in English")
    address: str = Field(..., description="Address of the pickup location")
    is_active: Optional[bool] = True  # Indicates if the pickup location is active
    lat: Optional[float] = None  # Latitude for the pickup location
    lon: Optional[float] = None  # Longitude for the pickup location

class PickUpLocationUpdate(BaseConfig):
    name_uz: Optional[str] = Field(None, description="Name of the pickup location in Uzbek")
    name_ru: Optional[str] = Field(None, description="Name of the pickup location in Russian")
    name_en: Optional[str] = Field(None, description="Name of the pickup location in English")
    address: Optional[str] = Field(None, description="Address of the pickup location")
    is_active: Optional[bool] = True  # Indicates if the pickup location is active
    lat: Optional[float] = None  # Latitude for the pickup location
    lon: Optional[float] = None  # Longitude for the pickup location