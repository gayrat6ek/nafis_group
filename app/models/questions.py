
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



class Questions(Base):
    __tablename__ = "questions"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), nullable=False)
    name = Column(String, nullable=False)  # Name of the person asking the question
    surname = Column(String, nullable=False)  # Surname of the person asking the question
    question_text = Column(String, nullable=False)
    answer_text = Column(String, nullable=True)  # Nullable if the question has not been answered yet
    is_answered = Column(Boolean, default=False)  # Indicates if the question has been answered

    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    likes = Column(Integer, default=0)  # Number of likes for the question
    dislikes = Column(Integer, default=0)  # Number of dislikes for the question

    product = relationship("Products", back_populates="questions")  # Assuming Products model has a questions relationship