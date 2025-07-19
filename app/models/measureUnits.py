import uuid
from sqlalchemy import (
    Column,
    ForeignKey,
    DateTime,
    String,
    Boolean,
    Integer,
    Float
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class MeasureUnits(Base):
    __tablename__ = "measure_units"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title_uz = Column(String, nullable=True, unique=True)  # e.g., product kilogram
    title_ru = Column(String, nullable=True, unique=True)
    title_en = Column(String, nullable=True, unique=True)
    name_uz = Column(String, nullable=False, unique=True)  # e.g., 'kilogram', 'liter'
    name_ru = Column(String, nullable=True, unique=True)
    name_en = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    is_active = Column(Boolean, default=True)  # To mark if the unit is active or not
    product_details = relationship("ProductDetails", back_populates="measure_unit")  # Assuming

    

