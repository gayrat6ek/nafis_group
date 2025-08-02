
import uuid
from sqlalchemy import (
    Column,
    Float,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class Regions(Base):
    __tablename__ = 'regions'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name_en = Column(String, nullable=False)  # English name for the region
    name_ru = Column(String, nullable=False)  # Russian name for the region
    name_uz = Column(String, nullable=False)  # Uzbek name for the region
    is_active = Column(Boolean, default=True)  # Indicates if the region is active
    delivery_cost = Column(Float, nullable=True, default=0.0)  # Default delivery cost for the region

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    districts = relationship("Districts", back_populates="region")  # Assuming a Districts model exists