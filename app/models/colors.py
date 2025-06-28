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


class Colors(Base):
    __tablename__ = "colors"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name_uz = Column(String, nullable=False, unique=True)
    name_ru = Column(String, nullable=False, unique=True)
    name_en = Column(String, nullable=False, unique=True)

    is_active = Column(Boolean, default=True)
    code = Column(String, nullable=False)  # Assuming hex code is a string representation of the color

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    product_details = relationship("ProductDetails", back_populates="color")  # Assuming a ProductDetails model exists