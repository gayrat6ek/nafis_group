
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


class Otps(Base):
    __tablename__ = "otps"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    phone_number = Column(String, nullable=False)  # Phone number associated with the OTP
    otp_code = Column(String, nullable=False)  # The OTP code itself
    is_verified = Column(Boolean, default=False)  # Indicates if the OTP has been verified
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Additional fields can be added as needed