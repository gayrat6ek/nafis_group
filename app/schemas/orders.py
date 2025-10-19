
from datetime import date, datetime
from enum import Enum
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from .productDetails import ProductDetailsInOrders,GetSize, ProductDetailsInOrdersFull
from app.schemas.users import GetUser, GetUserFullDataInOrder
from app.schemas.loanMonths import LoanMonthsGet
from app.schemas.userLocations import UserLocation
from app.schemas.pickUpLocations import PickUpLocationGet




class BaseConfig(BaseModel):
    class Config:
        orm_mode = True


class PaymentMethod(str, Enum):
    CARD = 'card'
    CASH = 'cash'
    LOAN = 'loan'  # Assuming loan is a valid payment method
    PAYME = 'payme'  # Assuming payme is a valid payment method

class OrderStatus(str, Enum):
    FINISHED = 'inactive'
    ACTIVE = 'active'
    LOAN = 'loan'
    


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


class OrderFullItems(BaseConfig):
    id: Optional[UUID] = None
    product_detail: ProductDetailsInOrdersFull  # Basic data of the product detail
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
    item_ids: Optional[List[UUID]] = None  # List of item IDs in the order
    user: Optional[GetUserFullDataInOrder] = None  # Basic user information associated with the order
    deny_reason: Optional[str] = None  # Reason for order denial or cancellation
    loan_month: Optional[LoanMonthsGet] = None  # Loan month details if applicable
    pick_up_location: Optional[PickUpLocationGet] = None  # Pick-up location details if applicable
    user_location: Optional[UserLocation] = None  # User location details if applicable


class OrderResponse(OrdersGet):
    payment_url  : Optional[str] = None  # URL for payment processing, if applicable
    
    


class OrdersFullGet(BaseConfig):
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
    region: Optional[str] = None
    district: Optional[str] = None
    created_at: Optional[datetime] = None
    items: List[OrderFullItems] = []  # List of order items associated with the order
    loan_month_id: Optional[UUID] = None
    loan_month_percent: Optional[float] = 0.0
    loan_month_price: Optional[float] = 0.0
    item_ids: Optional[List[UUID]] = None  # List of item IDs in the order
    user: Optional[GetUserFullDataInOrder] = None  # Basic user information associated with the order
    deny_reason: Optional[str] = None  # Reason for order denial or cancellation
    loan_month: Optional[LoanMonthsGet] = None  # Loan month details if applicable
    pick_up_location: Optional[PickUpLocationGet] = None  # Pick-up location details if applicable
    user_location: Optional[UserLocation] = None  # User location details if applicable
    


class CartItemsSelect(BaseConfig):
    item_ids: List[UUID]  # List of product detail IDs to select in the cart
    loan_month_id: Optional[UUID] = None  # ID of the loan month used for payment, if applicable
    user_location_id: Optional[UUID] = None  # ID of the user's location for delivery, if applicable
    pick_up_location_id:Optional[UUID] = None  # ID of the address for delivery, if applicable




class OrderFilter(BaseConfig):
    order_number: Optional[int] = None  # Filter by order number
    is_paid: Optional[bool] = None  # Filter by payment status
    filter: Optional[OrderStatus]=None  # Filter by order status
    status: Optional[int] = None  # Filter by specific order status code (if applicable)
    paymenttype: Optional[PaymentMethod] = None  # Filter by payment method
    username: Optional[str] = None  # Filter by user's name
    created_at: Optional[date] = None  # Filter by creation date
    is_loan: Optional[bool] = None  # Filter by loan status
    page: int = 1
    size: int = 10




class UpdateOrder(BaseConfig):
    status: Optional[int] = Field(None, description="New status of the order")
    is_paid: Optional[bool] = Field(None, description="Payment status of the order")
    is_delivered: Optional[bool] = Field(None, description="Delivery status of the order")
    description: Optional[str] = Field(None, max_length=500, description="Optional description for the order")
    payment_method: Optional[PaymentMethod] = Field(None, description="Payment method used for the order")
    delivery_address: Optional[str] = Field(None, max_length=255, description="Delivery address if applicable")
    delivery_phone_number: Optional[str] = Field(None, max_length=15, description="Phone number for delivery")
    delivery_receiver: Optional[str] = Field(None, max_length=100, description="Name of the person receiving the delivery")
    deny_reason: Optional[str] = Field(None, max_length=500, description="Reason for order denial or cancellation")
