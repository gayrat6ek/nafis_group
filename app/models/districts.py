import uuid
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Districts(Base):
    __tablename__ = 'districts'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name_en = Column(String, nullable=False)  # English name for the district
    name_ru = Column(String, nullable=False)  # Russian name for the district
    name_uz = Column(String, nullable=False)  # Uzbek name for the district

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    region_id = Column(UUID(as_uuid=True), ForeignKey('regions.id'), nullable=False)
    is_active = Column(Boolean, default=True)  # Indicates if the district is active
    region = relationship("Regions", back_populates="districts")  # Assuming a Regions model exists
    orders = relationship("Orders", back_populates="district")  # Assuming an Orders model exists with a district relationship