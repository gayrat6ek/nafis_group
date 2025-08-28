
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
    BIGINT,
    Table,
    Time,
    JSON,
    VARCHAR,
    Date,
DECIMAL,
BigInteger
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from datetime import datetime
from app.db.base import Base
import time


import pytz
import uuid


class Transactions(Base):
    __tablename__ = 'transactions'
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'))
    order = relationship('Orders', back_populates='transaction')
    amount = Column(DECIMAL,nullable=True)
    transaction_id = Column(String)
    create_time = Column(BigInteger, default=lambda: int(time.time() * 1000))
    perform_time = Column(BigInteger, default=0)
    cancel_time = Column(BigInteger,default=0)
    status = Column(Integer,default=0)
    reason= Column(Integer,nullable=True)
