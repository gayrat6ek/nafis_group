import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Float
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class DiscountProducts(Base):
    __tablename__ = "discount_products"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    discount_id = Column(UUID(as_uuid=True), ForeignKey('discounts.id'), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    discount = relationship("Discounts", back_populates="products")
    product = relationship("Products", back_populates="discounts")