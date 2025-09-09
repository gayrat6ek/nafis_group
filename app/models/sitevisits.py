
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
import uuid

class SiteVisits(Base):
    __tablename__ = "site_visits"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)

    ipaddress = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())

