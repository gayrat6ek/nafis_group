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
from app.models.Brands import Brands
from app.schemas.brands import CreateBrand, UpdateBrand


def create_brand(db: Session, data: CreateBrand) -> Brands:
    try:
        brand = Brands(
            name_en=data.name_en,
            name_ru=data.name_ru,
            name_uz=data.name_uz,
            description_en=data.description_en,
            description_ru=data.description_ru,
            description_uz=data.description_uz,
            image=data.image,
            is_active=data.is_active
        )
        db.add(brand)
        db.commit()
        db.refresh(brand)
        return brand
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    


def get_brands(db: Session, page: int = 1, size: int = 10,search:Optional[str]=None,is_active:Optional[bool]=None):
    try:
        query = db.query(Brands)
        if search is not None:
            query = query.filter(or_(
                Brands.name_en.ilike(f"%{search}%"),
                Brands.name_uz.ilike(f"%{search}%"),
                Brands.name_ru.ilike(f"%{search}%"),
                ))
        if is_active is not None:
            query = query.filter(Brands.is_active==is_active)
        total_count = query.count()
        query = query.order_by(Brands.name_en.asc())  # Order by English name by default
        brands = query.offset((page - 1) * size).limit(size).all()
        
        return {
            "items": brands,
            "total": total_count,
            "page": page,
            "size": size,
            'pages': (total_count + size - 1) // size 
        }
    except SQLAlchemyError as e:
        raise e
    

def get_brand_by_id(db: Session, brand_id: UUID) -> Optional[Brands]:
    try:
        return db.query(Brands).filter(Brands.id == brand_id).first()
    except SQLAlchemyError as e:
        raise e
    

def update_brand(db: Session, brand_id: UUID, data: UpdateBrand) -> Optional[Brands]:
    try:
        brand = db.query(Brands).filter(Brands.id == brand_id).first()
        if not brand:
            return None
        
        for key, value in data.dict(exclude_unset=True).items():
            setattr(brand, key, value)
        
        db.commit()
        db.refresh(brand)
        return brand
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def get_brand_by_name(db: Session, name_uz: str) -> Optional[Brands]:
    try:
        return db.query(Brands).filter(Brands.name_uz == name_uz).first()
    except SQLAlchemyError as e:
        raise e