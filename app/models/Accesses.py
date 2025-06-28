import uuid
from sqlalchemy import (
    Column,
    ForeignKey,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Accesses(Base):
    __tablename__ = "accesses"
    id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    permission_id = Column(UUID(as_uuid=True),ForeignKey('permissions.id'))
    permission = relationship('Permissions',back_populates='access')
    role_id = Column(UUID(as_uuid=True),ForeignKey('roles.id'))
    # role = relationship("Roles",back_populates="access")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

