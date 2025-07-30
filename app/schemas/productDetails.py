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


class GetSize(BaseConfig):
    id: Optional[UUID] = None
    value: str  # Assuming size is a string (e.g., "S", "M", "L")
    price: Optional[float] = None  # Optional price for the size
    curr_discount_price: Optional[float] = None  # Optional current discount price for the size
    loan_month: Optional[dict] = None  # Optional loan month information

    # there is is_deleted filed do not return size if it is True
    is_deleted: Optional[bool] = True  # Indicates if the size is deleted


class CreateSize(BaseConfig):
    value: str  # Required size value (e.g., "S", "M", "L")
    price: Optional[float] = None  # Optional price for the size
    detail_id: UUID  # Required to link the size to a product detail


class UpdateSize(BaseConfig):
    value: Optional[str] = None  # Optional to allow updating without changing the size value
    price: Optional[float] = None  # Optional to allow updating without changing the price


    



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





class ProductDetailsList(BaseConfig):
    id: UUID
    product_id: Optional[UUID] = None
    # sizes:Optional[str]=None

    video_info: Optional[list] = None

    images: Optional[list] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    color_id: Optional[UUID] = None  # Assuming product details are linked to colors
    # price: Optional[float] = None  # Assuming product details have a price
    quantity: Optional[float] = None  # Assuming product details have a quantity
    color:Optional[ColorGet] = None  # Assuming product details can have a color relationship
    measure_unit: Optional[getBasicMeasureUnits] = None  # Assuming product details can have a measure unit relationship
    size:Optional[List[GetSize]] = None  # Assuming product details can have multiple sizes
    



class CreateProductDetails(BaseConfig):
    product_id: UUID  # Required to link the product detail to a product
    # sizes:Optional[str]=None

    video_info: Optional[list] = None

    images: Optional[list] = None
    is_active: Optional[bool] = True
    color_id: Optional[UUID] = None  # Required to link the product detail to a color
    # price: Optional[float] = None  # Required for the product detail price
    quantity: Optional[float] = None  # Required for the product detail quantity
    measure_unit_id: Optional[UUID] = None  # Optional to allow creation without a measure unit
    #size input dict inside list and value and price inside of dict
    size: Optional[List[dict]] = Field(
        default=None, 
        description="List of size dictionaries, each containing 'value' and 'price' keys. Example: [{'value': 'S', 'price': 10.0}, {'value': 'M', 'price': 12.0}]")




class UpdateProductDetails(BaseConfig):
    # sizes:Optional[str]=None

    video_info: Optional[list] = None

    images: Optional[list] = None
    is_active: Optional[bool] = True
    color_id: Optional[UUID] = None  # Optional to allow updating without changing the color
    # price: Optional[float] = None  # Optional to allow updating without changing the price
    quantity: Optional[float] = None  # Optional to allow updating without changing the quantity
    measure_unit_id: Optional[UUID] = None  # Optional to allow updating without changing the measure unit
    size: Optional[List[UpdateSize]] = None  # Optional to allow updating without changing the sizes




class ProductDetailsBasicData(BaseConfig):
    id: UUID
    # sizes:Optional[str]=None
    video_info: Optional[list] = None
    images: Optional[list] = None
    is_active: Optional[bool] = True
    # price: Optional[float] = None  # Assuming product details have a price
    color:Optional[ColorGet] = None  # Assuming product details can have a color relationship
    measure_unit: Optional[getBasicMeasureUnits] = None  # Assuming product details can have a measure unit relationship
    size: Optional[List[GetSize]] = None  # Assuming product details can have multiple sizes




class ProductDetailsInOrders(BaseConfig):
    id: UUID
    images: Optional[list] = None
    is_active: Optional[bool] = True
    color:Optional[ColorGet] = None  # Assuming product details can have a color relationship
    measure_unit: Optional[getBasicMeasureUnits] = None  # Assuming product details can have a measure unit relationship