import uuid

from sqlalchemy import (
    Column,
    String,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class PermissionPages(Base):
    __tablename__ = "permission_pages"
    id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    name = Column(String,unique=True)
    description = Column(String, nullable = True)
    permission = relationship("Permissions",back_populates='permission_page')
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())