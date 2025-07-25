import uuid
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    String,
    DateTime,
    Boolean,
    
)
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Sizes(Base):
    __tablename__ = 'sizes'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    value = Column(String, nullable=False)  # Name of the size (e.g., "Small", "Medium", "Large")
    price = Column(Float, nullable=True)  # Optional price associated with the size
    detail_id = Column(UUID(as_uuid=True), ForeignKey('product_details.id'), nullable=False)  # Foreign key to ProductDetails

    product_details = relationship("ProductDetails", back_populates="size")  # Assuming ProductDetails has a size relationship
    is_deleted = Column(Boolean, default=False)  # Indicates if the size is deleted
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    order_items = relationship("OrderItems", back_populates="size")  # Assuming OrderItems model has a size relationship