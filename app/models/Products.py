import uuid
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base



class Products(Base):
    __tablename__ = 'products'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name_en = Column(String, nullable=True)  # English name for the product
    name_ru = Column(String, nullable=True)  # Russian name for the product
    name_uz = Column(String, nullable=True)  # Uzbek name for the product



    description_en = Column(String, nullable=True)  # English description
    description_ru = Column(String, nullable=True)  # Russian description
    description_uz = Column(String, nullable=True)  # Uzbek description


    delivery_days = Column(String, nullable=True)  # Estimated delivery days
    is_active = Column(Boolean, default=True)
    loan_accessable = Column(Boolean, default=True)
    characteristics = Column(JSONB, nullable=True)  # Assuming characteristics are stored as a JSON object
    views = Column(Integer, default=0)  # Number of views for the product



    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)

    # files = relationship("Files", back_populates="product")
    category = relationship("Categories", back_populates="products")
    discounts = relationship("DiscountProducts", back_populates="product")
    brand = relationship("Brands", back_populates="products")
    ratings = relationship("Ratings", back_populates="product")
    details = relationship("ProductDetails", back_populates="product")
    questions = relationship("Questions", back_populates="product")  
    materials = relationship("ProductMaterials", back_populates="product")  
    likes = relationship("Likes", back_populates="product")  # Assuming Likes model has a product relationship
    reviews = relationship("Reviews", back_populates="product")  # Assuming Reviews model has a product relationship





