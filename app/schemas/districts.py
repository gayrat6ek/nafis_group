
from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

class DistrictGet(BaseConfig):
    id: Optional[UUID] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None  
    is_active: Optional[bool] = True 
    region_id: Optional[UUID] = None  # Assuming districts are linked to regions    

class DistrictsList(BaseConfig):
    id: UUID
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    region_id: Optional[UUID] = None  # Assuming districts are linked to regions
    

class CreateDistrict(BaseConfig):
    name_uz: str
    name_ru: str
    name_en: str
    is_active: Optional[bool] = True
    region_id: UUID  # Required to link the district to a region


    
class UpdateDistrict(BaseConfig):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    is_active: Optional[bool] = True
    region_id: Optional[UUID] = None  # Optional to allow updating without changing the region
