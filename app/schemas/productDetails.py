from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from .colors import ColorGet
from .measureUnits import getBasicMeasureUnits


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

class ProductDetailsGet(BaseConfig):
    id: Optional[UUID] = None
    product_id: Optional[UUID] = None
    sizes:Optional[str]=None

    video_info: Optional[list] = None

    images: Optional[list] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    color_id: Optional[UUID] = None  # Assuming product details are linked to colors
    price: Optional[float] = None  # Assuming product details have a price
    quantity: Optional[float] = None  # Assuming product details have a quantity
    color:Optional[ColorGet] = None  # Assuming product details can have a color relationship
    measure_unit: Optional[getBasicMeasureUnits] = None  # Assuming product details can have a measure unit relationship


class ProductDetailsList(BaseConfig):
    id: UUID
    product_id: Optional[UUID] = None
    sizes:Optional[str]=None

    video_info: Optional[list] = None

    images: Optional[list] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    color_id: Optional[UUID] = None  # Assuming product details are linked to colors
    price: Optional[float] = None  # Assuming product details have a price
    quantity: Optional[float] = None  # Assuming product details have a quantity
    color:Optional[ColorGet] = None  # Assuming product details can have a color relationship
    measure_unit: Optional[getBasicMeasureUnits] = None  # Assuming product details can have a measure unit relationship



class CreateProductDetails(BaseConfig):
    product_id: UUID  # Required to link the product detail to a product
    sizes:Optional[str]=None

    video_info: Optional[list] = None

    images: Optional[list] = None
    is_active: Optional[bool] = True
    color_id: Optional[UUID] = None  # Required to link the product detail to a color
    price: Optional[float] = None  # Required for the product detail price
    quantity: Optional[float] = None  # Required for the product detail quantity
    measure_unit_id: Optional[UUID] = None  # Optional to allow creation without a measure unit


class UpdateProductDetails(BaseConfig):
    sizes:Optional[str]=None

    video_info: Optional[list] = None

    images: Optional[list] = None
    is_active: Optional[bool] = True
    color_id: Optional[UUID] = None  # Optional to allow updating without changing the color
    price: Optional[float] = None  # Optional to allow updating without changing the price
    quantity: Optional[float] = None  # Optional to allow updating without changing the quantity
    measure_unit_id: Optional[UUID] = None  # Optional to allow updating without changing the measure unit




class ProductDetailsBasicData(BaseConfig):
    id: UUID
    sizes:Optional[str]=None
    video_info: Optional[list] = None
    images: Optional[list] = None
    is_active: Optional[bool] = True
    price: Optional[float] = None  # Assuming product details have a price
    color:Optional[ColorGet] = None  # Assuming product details can have a color relationship
    measure_unit: Optional[getBasicMeasureUnits] = None  # Assuming product details can have a measure unit relationship