import uuid
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    DateTime,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class BankCards(Base):
    __tablename__ = "bank_cards"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    card_number = Column(String, nullable=False, unique=True)  # Assuming card number is stored as a string
    cardholder_name = Column(String, nullable=False)  # Name of the cardholder
    expiration_date = Column(String, nullable=False)  # Expiration date of the card
    cvv = Column(String, nullable=False)  # CVV of the card
    is_active = Column(Boolean, default=True)  # Whether the card is active or not
    card_phone_number = Column(String, nullable=True)  # Phone number associated with the card, if applicable
    is_verified = Column(Boolean, default=False)  # Whether the card is verified or not

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("Users", back_populates="bank_cards")  # Assuming Users model has a bank_cards relationship