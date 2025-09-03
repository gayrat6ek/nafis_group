import uuid
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Boolean,
    
)
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Reviews(Base):
    __tablename__ = 'reviews'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    product_detail_id = Column(UUID(as_uuid=True), ForeignKey('product_details.id'), nullable=True)
    rating = Column(Integer, nullable=False)  # Rating out of 5
    comment = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)  # Indicates if the review is active or deleted
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    images = Column(JSONB, nullable=True)  # Assuming images are stored as a JSON array of URLs or paths
    answer = Column(String, nullable=True)  # Admin's answer to the review, if applicable
    

    user = relationship("Users", back_populates="reviews")  # Assuming Users model has a reviews relationship
    product = relationship("Products", back_populates="reviews")
    product_detail = relationship("ProductDetails", back_populates="reviews")  # Assuming ProductDetails model has a reviews relationship