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


class Brands(Base):
    __tablename__ = "brands"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name_uz = Column(String, nullable=False, unique=True)
    name_ru = Column(String, nullable=False, unique=True)
    name_en = Column(String, nullable=False, unique=True)

    description_uz = Column(String, nullable=True)
    description_ru = Column(String, nullable=True)
    description_en = Column(String, nullable=True)
    
    is_active = Column(Boolean, default=True)
    image = Column(String, nullable=True)  # Assuming image is a URL or path to the image

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    products = relationship("Products", back_populates="brand")  # Assuming Products model has a brand relationship