


from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class MeasureUnitsGet(BaseConfig):
    id: Optional[UUID] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None

class MeasureUnitsList(BaseConfig):
    id: UUID
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None


class CreateMeasureUnits(BaseConfig):
    name_uz: str
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    is_active: Optional[bool] = True

    
class UpdateMeasureUnits(BaseConfig):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    is_active: Optional[bool] = True 


class getBasicMeasureUnits(BaseConfig):
    id: UUID
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None

    class Config:
        orm_mode = True 