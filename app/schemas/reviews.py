from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.colors import ColorGet
from app.schemas.measureUnits import getBasicMeasureUnits
from app.schemas.users import GetUser


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )   

class GetSize(BaseConfig):
    id: Optional[UUID] = None
    value: str  # Assuming size is a string (e.g., "S", "M", "L")
    price: Optional[float] = None  # Optional price for the size
    curr_discount_price: Optional[float] = None  # Optional current discount price for the size
    loan_months: Optional[list] = None  # Optional loan month information
    discount: Optional[float] = None  # Optional discount percentage for the size







class ProductDetailsGet(BaseConfig):
    id: Optional[UUID] = None

    video_info: Optional[list] = None

    images: Optional[list] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    color_id: Optional[UUID] = None  # Assuming product details are linked to colors
    price: Optional[float] = None  # Assuming product details have a price
    quantity: Optional[float] = None  # Assuming product details have a quantity
    color:Optional[ColorGet] = None  # Assuming product details can have a color relationship
    measure_unit: Optional[getBasicMeasureUnits] = None  # Assuming product details can have a measure unit relationship
    size: Optional[List[GetSize]] = None  # Assuming product details can have multiple sizes

class ProductBasicGet(BaseConfig):
    id: Optional[UUID] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None        
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    details:Optional[List[ProductDetailsGet]]=None




class ReviewGet(BaseConfig):
    id: Optional[UUID] = None
    rating: Optional[int] = Field(..., ge=1, le=5, description="Rating of the product from 1 to 5")
    comment: Optional[str] = Field(None, max_length=500, description="Comment about the product")
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    
    images: Optional[List[str]] = Field(None, description="List of image URLs or paths associated with the review")
    user: Optional[GetUser] = None  # Assuming reviews are linked to users


class CreateReview(BaseConfig):
    product_id: UUID = Field(..., description="ID of the product being reviewed")
    product_detail_id: Optional[UUID] = Field(None, description="ID of the specific product detail being reviewed")
    rating: int = Field(..., ge=1, le=5, description="Rating of the product from 1 to 5")
    comment: Optional[str] = Field(None, max_length=500, description="Comment about the product")
    images: Optional[List[str]] = Field(None, description="List of image URLs or paths associated with the review")




class UpdateReview(BaseConfig):
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating of the product from 1 to 5")
    comment: Optional[str] = Field(None, max_length=500, description="Comment about the product")
    is_active: Optional[bool] = True
    images: Optional[List[str]] = Field(None, description="List of image URLs or paths associated with the review")
    answer: Optional[str] = Field(None, max_length=500, description="Answer to the review, if applicable")




class ReviewAdminGet(BaseConfig):
    id: Optional[UUID] = None
    rating: Optional[int] = Field(..., ge=1, le=5, description="Rating of the product from 1 to 5")
    comment: Optional[str] = Field(None, max_length=500, description="Comment about the product")
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    product:Optional[ProductBasicGet]=None
    images: Optional[List[str]] = Field(None, description="List of image URLs or paths associated with the review")
    user: Optional[GetUser] = None  # Assuming reviews are linked to users
