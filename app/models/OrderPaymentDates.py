
import uuid
from sqlalchemy import (
    Column,
    ForeignKey,
    DateTime,
    Sequence,
    String,
    Boolean,
    Integer,
    Float
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class OrderPaymentDates(Base):
    __tablename__ = "order_payment_dates"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=False)
    amount = Column(Float, nullable=False)
    is_paid = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    order = relationship("Orders", back_populates="payment_dates")