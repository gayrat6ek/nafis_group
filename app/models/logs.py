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


class Logs(Base):
    __tablename__ = "logs"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    action = Column(String, nullable=False)  # e.g., 'create', 'update', 'delete'
    created_at = Column(DateTime(timezone=True), default=func.now())
    status = Column(Integer, nullable=False)  # e.g., 'success', 'failure'

    user = relationship("Users", back_populates="logs")  # Assuming Users model has a logs relationship
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=True)  # Optional, if the log is related to an order
    order = relationship("Orders", back_populates="logs")  # Assuming Orders model has