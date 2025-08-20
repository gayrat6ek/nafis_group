
from datetime import datetime
from enum import Enum
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from .productDetails import ProductDetailsInOrders,GetSize



class BaseConfig(BaseModel):
    class Config:
        orm_mode = True


class PaymentMethod(str, Enum):
    CARD = 'card'
    CASH = 'cash'
    LOAN = 'loan'  # Assuming loan is a valid payment method
    PAYME = 'payme'  # Assuming payme is a valid payment method
    


class AddOrUpdateCartItem(BaseConfig):
    product_detail_id: UUID
    quantity: int = Field(..., ge=1, description="Quantity of the product to add to the cart")
    size_id: UUID  # Optional size for the item


class RemoveCartItem(BaseConfig):
    item_id:UUID  # Optional size for the item, if applicable




class ConfirmOrder(BaseConfig):
    pick_up_location_id:Optional[UUID] = None  # ID of the address for delivery, if applicable
    payment_method: Optional[PaymentMethod] = Field(..., description="Payment method used for the order")
    description: Optional[str] = Field(None, max_length=500, description="Optional description for the order")
    delivery_address: Optional[str] = Field(None, max_length=255, description="Delivery address if applicable")
    delivery_phone_number: Optional[str] = Field(None, max_length=15, description="Phone number for delivery")
    # delivery_date: Optional[datetime] = None
    delivery_receiver: Optional[str] = Field(None, max_length=100, description="Name of the person receiving the delivery")
    bank_card_id: Optional[UUID] = None  # ID of the bank card used for payment, if applicable
    item_ids: Optional[List[UUID]] = None  # List of product detail IDs to confirm in the order
    loan_month_id: Optional[UUID] = None  # ID of the loan month used for payment, if applicable
    user_location_id: Optional[UUID] = None  # ID of the user's location for delivery, if applicable



   


class OrderItems(BaseConfig):
    id: Optional[UUID] = None
    product_detail: ProductDetailsInOrders  # Basic data of the product detail
    quantity: int = Field(..., ge=1, description="Quantity of the product in the order")
    price: float = Field(..., gt=0, description="Price of the product at the time of order")
    size: GetSize


class OrdersGet(BaseConfig):
    id: Optional[UUID] = None
    order_number: Optional[int] = None
    description: Optional[str] = None
    user_id: Optional[UUID] = None
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
    loan_month_id: Optional[UUID] = None
    loan_month_percent: Optional[float] = 0.0
    loan_month_price: Optional[float] = 0.0

    






