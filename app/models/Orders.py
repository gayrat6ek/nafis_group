
import uuid
from sqlalchemy import (
    Column,
    ForeignKey,
    DateTime,
    Sequence,
    String,
    Boolean,
    Integer,
    Float,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

order_num_seq = Sequence(
    'order_num_seq',
    start=100000,
    metadata=Base.metadata
)

class Orders(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    order_number = Column(
        Integer,
        order_num_seq,
        server_default=order_num_seq.next_value(),
        unique=True,
        nullable=False
    )
    description = Column(String, nullable=True)  # Description of the order
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)

    delivery_address = Column(String, nullable=True)  # Full address for delivery
    delivery_phone_number = Column(String, nullable=True)  # Phone number for delivery contact
    delivery_receiver = Column(String, nullable=True)  # Name of the person receiving the delivery
    delivery_date = Column(DateTime(timezone=True), nullable=True)
    delivery_fee = Column(Float, nullable=False, default=0.0)
    region = Column(String, nullable=True)  # Region for delivery
    district = Column(String, nullable=True)  # District for delivery

    payment_method = Column(String, nullable=True)  # e.g., 'credit_card', 'cash', etc.
    discount_amount = Column(Float, nullable=True, default=0.0)  # Amount of discount applied to the order

    items_count = Column(Integer, nullable=False, default=0)  # Total number of items in the order
    total_items_price = Column(Float, nullable=False, default=0.0)  # Total price of items before any discounts or fees
    total_discounted_price = Column(Float, nullable=False, default=0.0)  # Total price after applying discounts
    total_amount = Column(Float, nullable=True)
    pick_up_location_id = Column(UUID(as_uuid=True), ForeignKey('pick_up_locations.id'), nullable=True)
    loan_month_id = Column(UUID(as_uuid=True), ForeignKey('loan_months.id'), nullable=True)
    loan_month_percent = Column(Float, nullable=True, default=0.0)
    loan_month_price = Column(Float, nullable=True, default=0.0)
    status = Column(Integer, nullable=False)
    is_paid = Column(Boolean, default=False)
    is_delivered = Column(Boolean, default=False)  # Indicates if the order has been delivered
    user_location_id = Column(UUID(as_uuid=True), ForeignKey('user_locations.id'), nullable=True)
    item_ids = Column(JSONB, nullable=True)  # List of item IDs in the order

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    card_id = Column(UUID(as_uuid=True), ForeignKey('bank_cards.id'), nullable=True)  # ID of the bank card used for payment, if applicable
    deny_reason = Column(String, nullable=True)  # Reason for order denial or cancellation
    card = relationship("BankCards", back_populates="orders")  # Assuming BankCards model has an orders relationship
    confirm_number = Column(Integer, nullable=True)  # Confirm number of the order
    client_confirmed_date = Column(DateTime(timezone=True), nullable=True)  # Indicates if the client has confirmed the order
    confirm_status = Column(String, nullable=True)
    """
    confirm_status:
    - confirming
    - confirmed
    - null "this means this order is not for loan"
    """
    user = relationship("Users", back_populates="orders")
    payment_dates = relationship("OrderPaymentDates", back_populates="order")
    items = relationship("OrderItems", back_populates="order")
    logs = relationship("Logs", back_populates="order")  # Assuming Logs model has an order relationship
    pick_up_location = relationship("PickUpLocations", back_populates="orders")  # Assuming PickUpLocations model has an orders relationship
    user_location = relationship("UserLocations", back_populates="orders")
    loan_month = relationship("LoanMonths", back_populates="orders")
    transaction = relationship("Transactions", back_populates="order")  # Assuming Transactions model has an order relationship
    


"""
statuses

0 - In cart
1 - New
2 - confirmed
3 - prepared
4 - delivering
5 - delivered
6 - cancelled
7 - delived to branch
"""


