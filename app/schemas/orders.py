
from datetime import datetime
from enum import Enum
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from .productDetails import ProductDetailsInOrders,GetSize



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class PaymentMethod(str, Enum):
    card = 'card'
    cash = 'cash'


class AddOrUpdateCartItem(BaseConfig):
    product_detail_id: UUID
    quantity: int = Field(..., ge=1, description="Quantity of the product to add to the cart")
    size_id: UUID  # Optional size for the item


class RemoveCartItem(BaseConfig):
    product_detail_id: UUID




class ConfirmOrder(BaseConfig):
    delivery_address: str = Field(..., min_length=1, max_length=255, description="Full address for delivery")
    delivery_phone_number: str = Field(..., min_length=10, max_length=15, description="Phone number for delivery contact")
    delivery_date: datetime = Field(..., description="Date and time for the delivery")
    payment_method: Optional[PaymentMethod] = Field(..., description="Payment method used for the order")
    discount_id: Optional[UUID] = None  # ID of the discount applied to the order, if any
    district_id: Optional[UUID] = None  # ID of the district for delivery, if applicable
    description: Optional[str] = Field(None, max_length=500, description="Optional description for the order")


    #filter payment methods only allow card, cash, 


class OrderItems(BaseConfig):
    product_detail: ProductDetailsInOrders  # Basic data of the product detail
    quantity: int = Field(..., ge=1, description="Quantity of the product in the order")
    price: float = Field(..., gt=0, description="Price of the product at the time of order")
    size: GetSize


class OrdersGet(BaseConfig):
    id: Optional[UUID] = None
    order_number: Optional[int] = None
    description: Optional[str] = None
    user_id: Optional[UUID] = None
    district_id: Optional[UUID] = None
    delivery_address: Optional[str] = None
    delivery_phone_number: Optional[str] = None
    delivery_date: Optional[datetime] = None
    delivery_fee: Optional[float] = 0.0
    payment_method: Optional[str] = None
    discount_amount: Optional[float] = 0.0
    items_count: Optional[int] = 0
    total_items_price: Optional[float] = 0.0
    total_discounted_price: Optional[float] = 0.0
    total_amount: Optional[float] = None
    status: Optional[int] = 0  # Assuming status is an integer representing the order status
    is_paid: Optional[bool] = False
    is_delivered: Optional[bool] = False
    created_at: Optional[datetime] = None
    items: List[OrderItems] = []  # List of order items associated with the order

    






