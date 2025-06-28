
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

class OrderItems(Base):
    __tablename__ = "order_items"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False) # Price per item at the time of order
    product_detail_id = Column(UUID(as_uuid=True), ForeignKey('product_details.id'), nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    

    order = relationship("Orders", back_populates="items")
    product_detail = relationship("ProductDetails", back_populates="order_items")  # Assuming ProductDetails model has an order_items relationship