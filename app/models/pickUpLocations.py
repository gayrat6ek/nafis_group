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


class PickUpLocations(Base):
    __tablename__ = "pick_up_locations"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name_uz = Column(String, nullable=False)
    name_ru = Column(String, nullable=False)
    name_en = Column(String, nullable=False)
    address = Column(String, nullable=False)  # Address of the pickup location
    is_active = Column(Boolean, default=True)  # Indicates if the pickup location is active
    lat = Column(Float, nullable=True)  # Latitude for the pickup location
    lon = Column(Float, nullable=True)  # Longitude for the pickup location
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    orders = relationship("Orders", back_populates="pick_up_location")  # Assuming Orders model has a pick_up_location relationship
    
    # Relationships can be added here if needed