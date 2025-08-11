import uuid
from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
    Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

class UserLocations(Base):
    __tablename__ = "user_locations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    
    # Location name (optional)
    location_name = Column(String, nullable=True)
    
    # Address details (all optional)
    street_address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state_province = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    country = Column(String, nullable=True)
    
    # Coordinates (optional)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    
    # Additional address information (optional)
    apartment_suite = Column(String, nullable=True)
    building_name = Column(String, nullable=True)
    floor_number = Column(String, nullable=True)
    
    # User relationship
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    user = relationship("Users", back_populates="user_locations")
    orders = relationship("Orders", back_populates="user_location")
    
    # Metadata
    is_default = Column(Boolean, default=False)  # Mark as default location
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
