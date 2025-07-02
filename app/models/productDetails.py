import uuid
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base



class ProductDetails(Base):
    __tablename__ = "product_details"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    size = Column(JSONB, nullable=True)  # Assuming size is stored as a JSON object (e.g., {"size": "M", "dimensions": {"length": 10, "width": 5}})
    is_active = Column(Boolean, default=True)  # Indicates if the product detail is active

    
    characteristics = Column(JSONB, nullable=True)  # Assuming characteristics are stored as a JSON object
    video_info = Column(JSONB, nullable=True)  # Assuming video information is stored as a JSON object
    images = Column(JSONB, nullable=True)  # Assuming images are stored as a JSON array of URLs or paths


    quantity = Column(Float, nullable=True)
    price = Column(Float, nullable=False)


    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    color_id = Column(UUID(as_uuid=True), ForeignKey('colors.id'), )
    
    color = relationship("Colors", back_populates="product_details")
    product = relationship("Products", back_populates="details")
    order_items = relationship("OrderItems", back_populates="product_detail")  # Assuming OrderItems model has a product_detail relationship