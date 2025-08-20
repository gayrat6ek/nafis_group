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
from app.models.regions import Regions
from app.schemas.regions import CreateRegion, UpdateRegion




def create_region(db: Session, data: CreateRegion) -> Regions:
    try:
        region = Regions(
            name_en=data.name_en,
            name_ru=data.name_ru,
            name_uz=data.name_uz,
            is_active=True,
            delivery_cost=data.delivery_cost if data.delivery_cost is not None else 0.0,  # Default to 0.0 if not provided
            delivery_days=data.delivery_days
        )
        db.add(region)
        db.commit()
        db.refresh(region)
        return region
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_regions(db: Session, page: int = 1, size: int = 10,is_active:Optional[bool]=None) -> list[Regions]:
    try:
        query = db.query(Regions)
        if is_active is not None:
            query = query.filter(Regions.is_active == is_active)
        total_count = query.count()
        regions = query.offset((page - 1) * size).limit(size).all()
        
        return {
            "items": regions,
            "total": total_count,
            "page": page,
            "size": size,
            'pages': (total_count + size - 1) // size 
        }
    except SQLAlchemyError as e:
        raise e

def get_region_by_id(db: Session, region_id: UUID) -> Optional[Regions]:
    try:
        return db.query(Regions).filter(Regions.id == region_id).first()
    except SQLAlchemyError as e:
        raise e

def update_region(db: Session, region_id: UUID, data: UpdateRegion) -> Optional[Regions]:
    try:
        region = db.query(Regions).filter(Regions.id == region_id).first()
        if not region:
            return None
        
        for key, value in data.dict(exclude_unset=True).items():
            setattr(region, key, value)
        
        db.commit()
        db.refresh(region)
        return region
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def get_region_by_name(db: Session, name: str) -> Optional[Regions]:
    try:
        return db.query(Regions).filter(
            or_(
                Regions.name_en.ilike(f"%{name}%"),
                Regions.name_ru.ilike(f"%{name}%"),
                Regions.name_uz.ilike(f"%{name}%")
            )
        ).first()
    except SQLAlchemyError as e:
        raise e