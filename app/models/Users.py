import uuid
from sqlalchemy import (
    Column,
    Float,
    Integer,
    Sequence,
    String,
    ForeignKey,
    DateTime,
    Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base

user_num_seq = Sequence(
    'user_num_seq',
    start=100000,
    metadata=Base.metadata
)

class Users(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True),primary_key=True,index=True,default=uuid.uuid4)
    user_number = Column(
        Integer,
        user_num_seq,
        server_default=user_num_seq.next_value(),
        unique=True,
        nullable=False
    )
    username=Column(String,unique=True,nullable=False)
    full_name = Column(String,nullable=True)
    password = Column(String)
    role_id = Column(UUID(as_uuid=True),ForeignKey('roles.id'),nullable=True)
    is_client = Column(Boolean, default=True)  
    role = relationship('Roles',back_populates='user')
    passport_front_image = Column(String, nullable=True)
    passport_back_image = Column(String, nullable=True)
    person_passport_image = Column(String, nullable=True)
    passport_series = Column(String, nullable=True)

    phone_number = Column(String, nullable=True, unique=True)
    extra_phone_number = Column(String, nullable=True, unique=True)
    birth_date = Column(DateTime(timezone=True), nullable=True)  # Assuming birth date



    email = Column(String, nullable=True, unique=True)
    is_verified = Column(Boolean, default=False) 
    is_active = Column(Boolean, default=True)  
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    marriage_status = Column(String, nullable=True)  # Assuming marriage status is a string
    job = Column(String, nullable=True)  # Assuming occupation is a string
    salary = Column(String, nullable=True)  # Assuming salary is a string
    exerience = Column(Float, nullable=True)  # Assuming work experience is a string
    work_place = Column(String, nullable=True)  # Assuming workplace is a string

    bank_cards = relationship("BankCards", back_populates="user")  # Assuming BankCards model has a user relationship
    orders = relationship("Orders", back_populates="user")  # Assuming Orders model has
    logs = relationship("Logs", back_populates="user")  # Assuming Logs model has a user relationship

    
