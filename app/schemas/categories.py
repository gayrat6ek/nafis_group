from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict




class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

class CategoryGet(BaseConfig):
    id: Optional[UUID] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    image: Optional[str] = None  # Assuming image is a URL or path to the image
    parent_id: Optional[UUID] = None  # ID of the parent category, if any
    is_active: Optional[bool] = True  # Indicates if the category is active or not

class CategoryList(BaseConfig):
    id: UUID
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    image: Optional[str] = None  # Assuming image is a URL or path to the image
    parent_id: Optional[UUID] = None  # ID of the parent category, if any
    is_active: Optional[bool] = True  # Indicates if the category is active or not
    created_at: Optional[datetime] = None  # Timestamp when the category was created


class GetCategoriesTree(BaseConfig):
    id: UUID
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    image: Optional[str] = None  # Assuming image is a URL or path to the image
    parent_id: Optional[UUID] = None  # ID of the parent category, if any
    is_active: Optional[bool] = True  # Indicates if the category is active or not
    # children: Optional[List['GetCategoriesTree']] = []  # List of child categories, if any
    parent: Optional['GetCategoriesTree'] = None  # Parent category, if any

    class Config:
        orm_mode = True  # Enable ORM mode for compatibility with SQLAlchemy models

class CreateCategory(BaseConfig):
    name_uz: str
    name_ru: str
    name_en: str
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    image: Optional[str] = None  # Assuming image is a URL or path to the image
    parent_id: Optional[UUID] = None  # ID of the parent category, if any
    is_active: Optional[bool] = True  # Indicates if the category is active or not


class UpdateCategory(BaseConfig):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    image: Optional[str] = None  # Assuming image is a URL or path to the image
    parent_id: Optional[UUID] = None  # ID of the parent category, if any
    is_active: Optional[bool] = True  # Indicates if the category is active or not


class FilterCategory(BaseConfig):
    search: Optional[str] = None  # Search term to filter categories by name or description
    is_active: Optional[bool] = None  # Filter by active status of the category
    parent_id: Optional[UUID] = None 