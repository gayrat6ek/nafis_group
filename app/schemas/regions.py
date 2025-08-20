from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )
class RegionGet(BaseConfig):
    id: Optional[UUID] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None  
    is_active: Optional[bool] = True 
    delivery_cost: Optional[float] = Field(0.0, description="Default delivery cost for the region")
    delivery_days: Optional[int] = Field(0, description="Default delivery days for the region")

class RegionsList(BaseConfig):
    id: UUID
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    delivery_cost: Optional[float] = Field(0.0, description="Default delivery cost for the region")
    delivery_days: Optional[int] = Field(0, description="Default delivery days for the region")


class CreateRegion(BaseConfig):
    name_uz: str
    name_ru: str
    name_en: str
    is_active: Optional[bool] = True
    delivery_cost: Optional[float] = Field(0.0, description="Default delivery cost for the region")
    delivery_days: Optional[int] = Field(0, description="Default delivery days for the region")


class UpdateRegion(BaseConfig):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    is_active: Optional[bool] = True

    delivery_cost: Optional[float] = Field(None, description="Default delivery cost for the region")
    delivery_days: Optional[int] = Field(0, description="Default delivery days for the region")
