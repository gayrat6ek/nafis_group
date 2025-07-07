from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict

class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )



class ProductGet(BaseConfig):
    id: Optional[UUID] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None        
    description_ru: Optional[str] = None
    description_en: Optional[str] = None

    delivery_days: Optional[int] = None
    is_active: Optional[bool] = True
    loan_accessable: Optional[bool] = True
    category_id: Optional[UUID] = None  # Assuming products are linked to categories
    brand_id: Optional[UUID] = None  # Assuming products are linked to brands
    created_at: Optional[datetime] = None


class DiscountProducts(BaseConfig):
    product: Optional[ProductGet] = None  # Assuming discounts can be linked to products

class DiscountGet(BaseConfig):
    id: Optional[UUID] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    is_news: Optional[bool] = False  # Assuming this is a flag for news or special discounts
    is_active: Optional[bool] = True
    amount: Optional[float] = None  # Assuming discounts have an amount field
    created_at: Optional[datetime] = None
    active_from: Optional[datetime] = None  # Assuming discounts have a start date
    active_to: Optional[datetime] = None  # Assuming discounts have an end date
    image : Optional[str] = None  # Assuming discounts have an image field
    products: Optional[List[DiscountProducts]] = None  # Assuming discounts can be linked to multiple products

class DiscountList(BaseConfig):
    id: UUID
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    is_news: Optional[bool] = False  # Assuming this is a flag for news or special discounts
    is_active: Optional[bool] = True
    amount: Optional[float] = None  # Assuming discounts have an amount field
    created_at: Optional[datetime] = None
    active_from: Optional[datetime] = None  # Assuming discounts have a start date
    active_to: Optional[datetime] = None  # Assuming discounts have an end date
    image : Optional[str] = None  # Assuming discounts have an image field


class CreateDiscount(BaseConfig):
    name_uz: str
    name_ru: str
    name_en: str
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    is_news: Optional[bool] = False  # Assuming this is a flag for news or special discounts
    is_active: Optional[bool] = True
    amount: float  # Required for the discount amount
    active_from: Optional[datetime] = None  # Required for the start date of the discount
    active_to: Optional[datetime] = None  # Required for the end date of the discount
    image : Optional[str] = None  # Assuming discounts have an image field
    product_ids: Optional[List[UUID]] = None  # Assuming discounts can be linked to multiple products


class UpdateDiscount(BaseConfig):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    is_news: Optional[bool] = False  # Assuming this is a flag for news or special discounts
    is_active: Optional[bool] = True
    amount: Optional[float] = None  # Optional to allow updating without changing the amount
    active_from: Optional[datetime] = None  # Optional to allow updating without changing the start date
    active_to: Optional[datetime] = None  # Optional to allow updating without changing the end date
    image : Optional[str] = None  # Assuming discounts have an image field
    product_ids: Optional[List[UUID]] = None  # Optional to allow updating without changing the linked products



