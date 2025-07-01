from pickletools import read_unicodestringnl

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.models.colors import Colors
from app.schemas.colors import CreateColor, UpdateColor


def create_color(db: Session, data: CreateColor) -> Colors:
    try:
        color = Colors(
            name_en=data.name_en,
            name_ru=data.name_ru,
            name_uz=data.name_uz,
            code=data.code,
            is_active=data.is_active
        )
        db.add(color)
        db.commit()
        db.refresh(color)
        return color
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def get_colors(db: Session, is_active: Optional[bool] = None):
    try:
        query = db.query(Colors)
        if is_active is not None:
            query = query.filter(Colors.is_active == is_active)
        
        return query.all()
        
    except SQLAlchemyError as e:
        raise e
    

def get_color_by_id(db: Session, color_id: UUID) -> Optional[Colors]:
    try:
        return db.query(Colors).filter(Colors.id == color_id).first()
    except SQLAlchemyError as e:
        raise e
    


def update_color(db: Session, color_id: UUID, data: UpdateColor) -> Optional[Colors]:
    try:
        color = db.query(Colors).filter(Colors.id == color_id).first()
        if not color:
            return None
        
        for key, value in data.dict(exclude_unset=True).items():
            setattr(color, key, value)
        
        db.commit()
        db.refresh(color)
        return color
    except SQLAlchemyError as e:
        db.rollback()
        raise e