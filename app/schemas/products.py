from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.brands import BrandGet
from app.schemas.categories import CategoryGet
from app.schemas.productDetails import ProductDetailsBasicData


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

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
    active_to: Optional[datetime] = None 









class DiscountsProducts(BaseConfig):
    discount: Optional[DiscountGet] = None  # Assuming discounts can be linked to products


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
    category:Optional[CategoryGet]=None
    brand:Optional[BrandGet]=None
    discounts: Optional[List[DiscountsProducts]] = None  # Assuming products can have multiple discounts
    details: Optional[List[ProductDetailsBasicData]] = None  # Assuming products can have details


class ProductList(BaseConfig):
    id: UUID
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
    discounts: Optional[List[DiscountsProducts]] = None  # Assuming products can have multiple discounts
    details: Optional[List[ProductDetailsBasicData]] = None  # Assuming products can have details



class CreateProduct(BaseConfig):
    name_uz: str
    name_ru: str
    name_en: str
    description_uz: Optional[str] = None        
    description_ru: Optional[str] = None
    description_en: Optional[str] = None

    delivery_days: Optional[int] = None
    is_active: Optional[bool] = True
    loan_accessable: Optional[bool] = True
    category_id: UUID  # Required to link the product to a category
    brand_id: UUID  # Required to link the product to a brand


class UpdateProduct(BaseConfig):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None        
    description_ru: Optional[str] = None
    description_en: Optional[str] = None

    delivery_days: Optional[int] = None
    is_active: Optional[bool] = True
    loan_accessable: Optional[bool] = True
    category_id: Optional[UUID] = None  # Optional to allow updating without changing the category
    brand_id: Optional[UUID] = None  # Optional to allow updating without changing the brand