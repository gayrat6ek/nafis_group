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
from app.models.districts import Districts
from app.schemas.districts import CreateDistrict, UpdateDistrict

def create_district(db: Session, data: CreateDistrict) -> Districts:
    try:
        district = Districts(
            name_en=data.name_en,
            name_ru=data.name_ru,
            name_uz=data.name_uz,
            region_id=data.region_id,
            is_active=True
        )
        db.add(district)
        db.commit()
        db.refresh(district)
        return district
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def get_districts(db: Session,region_id:Optional[UUID]=None, page: int = 1, size: int = 10, is_active:Optional[bool]=None) -> list[Districts]:
    try:
        query = db.query(Districts)
        if region_id:
            query = query.filter(Districts.region_id == region_id)
        if is_active is not None:
            query = query.filter(Districts.is_active == is_active)
        
        total_count = query.count()
        districts = query.offset((page - 1) * size).limit(size).all()
        
        return {
            "items": districts,
            "total": total_count,
            "page": page,
            "size": size,
            'pages': (total_count + size - 1) // size 
        }
    except SQLAlchemyError as e:
        raise e
    

def get_district_by_id(db: Session, district_id: UUID) -> Optional[Districts]:
    try:
        return db.query(Districts).filter(Districts.id == district_id).first()
    except SQLAlchemyError as e:
        raise e
    

def update_district(db: Session, district_id: UUID, data: UpdateDistrict) -> Optional[Districts]:
    try:
        district = db.query(Districts).filter(Districts.id == district_id).first()
        if not district:
            return None
        
        for key, value in data.dict(exclude_unset=True).items():
            setattr(district, key, value)
        
        db.commit()
        db.refresh(district)
        return district
    except SQLAlchemyError as e:
        db.rollback()
        raise e