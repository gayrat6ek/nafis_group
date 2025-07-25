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
    is_active = Column(Boolean, default=True)  # Indicates if the product detail is active
    # sizes =Column(String, nullable=True)  # Assuming sizes are stored as a comma-separated string (e.g., "S,M,L,XL")
    

    
    video_info = Column(JSONB, nullable=True)  # Assuming video information is stored as a JSON object
    images = Column(JSONB, nullable=True)  # Assuming images are stored as a JSON array of URLs or paths


    quantity = Column(Float, nullable=True)
    # price = Column(Float, nullable=False)


    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    color_id = Column(UUID(as_uuid=True), ForeignKey('colors.id'), )

    measure_unit_id = Column(UUID(as_uuid=True), ForeignKey('measure_units.id'), nullable=True)
    
    color = relationship("Colors", back_populates="product_details")
    product = relationship("Products", back_populates="details")
    order_items = relationship("OrderItems", back_populates="product_detail")  # Assuming OrderItems model has a product_detail relationship
    measure_unit = relationship("MeasureUnits", back_populates="product_details")  # Assuming MeasureUnits model has a product_details relationship
    size = relationship("Sizes", back_populates="product_details")  # Assuming Sizes model has a product_details relationship