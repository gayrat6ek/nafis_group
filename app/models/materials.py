
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


class Materials(Base):
    __tablename__ = "materials"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name_uz = Column(String, nullable=False, unique=True)  # e.g., 'steel', 'wood'
    name_ru = Column(String, nullable=True, unique=True)
    name_en = Column(String, nullable=True, unique=True)

    created_at = Column(DateTime(timezone=True), default=func.now())
    is_active = Column(Boolean, default=True)  # To mark if the material is active or not

    products = relationship("ProductMaterials", back_populates="material")  # Assuming a ProductMaterials model exists