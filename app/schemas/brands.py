
from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

class BrandGet(BaseConfig):
    id: Optional[UUID] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    image: Optional[str] = None  # Assuming image is a URL or path to the image
    is_active: Optional[bool] = True  # Indicates if the brand is active or not


class CreateBrand(BaseConfig):
    name_uz: str = Field(..., min_length=1, max_length=255)
    name_ru: str = Field(..., min_length=1, max_length=255)
    name_en: str = Field(..., min_length=1, max_length=255)
    description_uz: Optional[str] = Field(None, max_length=1000)
    description_ru: Optional[str] = Field(None, max_length=1000)
    description_en: Optional[str] = Field(None, max_length=1000)
    image: Optional[str] = None  # Assuming image is a URL or path to the image
    is_active: bool = True  # Indicates if the brand is active or not


class UpdateBrand(BaseConfig):
    name_uz: Optional[str] = Field(None, min_length=1, max_length=255)
    name_ru: Optional[str] = Field(None, min_length=1, max_length=255)
    name_en: Optional[str] = Field(None, min_length=1, max_length=255)
    description_uz: Optional[str] = Field(None, max_length=1000)
    description_ru: Optional[str] = Field(None, max_length=1000)
    description_en: Optional[str] = Field(None, max_length=1000)
    image: Optional[str] = None  # Assuming image is a URL or path to the image
    is_active: Optional[bool] = True  # Indicates if the brand is active or not


