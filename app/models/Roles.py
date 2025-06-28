import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    
)
from sqlalchemy.dialects.postgresql import UUID,JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Roles(Base):
    __tablename__ = 'roles'
    id = Column(UUID(as_uuid=True), primary_key=True, index = True,default=uuid.uuid4)
    name = Column(String)
    description = Column(String, nullable =True)
    is_active = Column(Boolean,default=True)
    # access = relationship("Accesses", back_populates="role")
    user = relationship("Users",back_populates='role')
    permissions = Column(JSONB, nullable=True)  # Store permissions as a JSONB field
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
