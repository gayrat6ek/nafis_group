import uuid
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Ratings(Base):
    __tablename__ = "ratings"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    name = Column(String, nullable=False)  # Name of the user or reviewer
    surname = Column(String, nullable=False)  # Surname of the user or reviewer
    rating = Column(Integer, nullable=False)  # Assuming rating is a float value
    comment = Column(String, nullable=True)  # Optional comment field
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    likes = Column(Integer, default=0)  # Number of likes for the rating
    dislikes = Column(Integer, default=0)  # Number of dislikes for the rating

    product = relationship("Products", back_populates="ratings")