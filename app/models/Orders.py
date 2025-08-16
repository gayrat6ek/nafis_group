
import uuid
from sqlalchemy import (
    Column,
    ForeignKey,
    DateTime,
    Sequence,
    String,
    Boolean,
    Integer,
    Float
)
from sqlalchemy.dialects.postgresql import UUID
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
    district_id = Column(UUID(as_uuid=True), ForeignKey('districts.id'), nullable=True)

    delivery_address = Column(String, nullable=True)  # Full address for delivery
    delivery_phone_number = Column(String, nullable=True)  # Phone number for delivery contact
    delivery_receiver = Column(String, nullable=True)  # Name of the person receiving the delivery
    delivery_date = Column(DateTime(timezone=True), nullable=True)
    delivery_fee = Column(Float, nullable=False, default=0.0)

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

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    card_id = Column(UUID(as_uuid=True), ForeignKey('bank_cards.id'), nullable=True)  # ID of the bank card used for payment, if applicable
    card = relationship("BankCards", back_populates="orders")  # Assuming BankCards model has an orders relationship
    
    user = relationship("Users", back_populates="orders")
    payment_dates = relationship("OrderPaymentDates", back_populates="order")
    district = relationship("Districts", back_populates="orders")
    items = relationship("OrderItems", back_populates="order")
    logs = relationship("Logs", back_populates="order")  # Assuming Logs model has an order relationship
    pick_up_location = relationship("PickUpLocations", back_populates="orders")  # Assuming PickUpLocations model has an orders relationship
    user_location = relationship("UserLocations", back_populates="orders")
    loan_month = relationship("LoanMonths", back_populates="orders")



"""
statuses

0 - new and in cart
1 - confirmed and awaiting payment
2 - delivery in progress
3 - delivered or completed
4 - cancelled
"""


