import uuid
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    DateTime,
    String
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base



class Categories(Base):
    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name_en = Column(String, nullable=True)  # English name for the category
    name_ru = Column(String, nullable=True)  # Russian name for the category
    name_uz = Column(String, nullable=True)  # Uzbek name for the category
    description_en = Column(String, nullable=True)  # English description
    description_ru = Column(String, nullable=True)  # Russian description
    description_uz = Column(String, nullable=True)  # Uzbek description
    image = Column(String, nullable=True)  # Assuming image is a URL or path to the image
    is_active = Column(Boolean, default=True)  # Indicates if the category is active
    parent_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'), nullable=True)
    parent = relationship("Categories", remote_side=[id], backref="children")
    is_child = Column(Boolean, default=False)  # Indicates if the category is a child of another category
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    products = relationship("Products", back_populates="category")

    