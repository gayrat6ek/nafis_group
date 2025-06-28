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


class LoanMonths(Base):
    __tablename__ = "loan_months"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    months = Column(Integer, nullable=False, unique=True)
    percent = Column(Float, nullable=False, unique=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())