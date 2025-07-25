import uuid
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Float
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Discounts(Base):
    __tablename__ = "discounts"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name_uz = Column(String, nullable=False, )
    name_ru = Column(String, nullable=False,)
    name_en = Column(String, nullable=False, )


    description_uz = Column(String, nullable=True)
    description_ru = Column(String, nullable=True)
    description_en = Column(String, nullable=True)
    is_news = Column(Boolean, default=False)  # Assuming this is a flag for news or special discounts

    is_active = Column(Boolean, default=True)
    amount = Column(Float, nullable=False)
    image = Column(String, nullable=True)  # Assuming image is a URL or path to the image

    active_from = Column(DateTime(timezone=True), nullable=False)
    active_to = Column(DateTime(timezone=True), nullable=False)


    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    products = relationship("DiscountProducts", back_populates="discount")

    