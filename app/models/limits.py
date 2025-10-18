import uuid
from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    DateTime,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Limits(Base):
    __tablename__ = "limits"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    limit = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())