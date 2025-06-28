import uuid

from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Permissions(Base):
    __tablename__ = "permissions"
    id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    name = Column(String,index=True)
    link = Column(String,nullable=True)
    permission_page_id = Column(UUID(as_uuid=True),ForeignKey('permission_pages.id'))
    permission_page = relationship("PermissionPages", back_populates='permission')
    access = relationship("Accesses",back_populates="permission")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
