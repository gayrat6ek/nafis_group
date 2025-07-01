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
from app.models.Categories import Categories
from app.schemas.categories import CreateCategory, UpdateCategory,FilterCategory


def create_category(db: Session, data: CreateCategory) -> Categories:
    try:
        category = Categories(
            name_en=data.name_en,
            name_ru=data.name_ru,
            name_uz=data.name_uz,
            description_en=data.description_en,
            description_ru=data.description_ru,
            description_uz=data.description_uz,
            image=data.image,
            parent_id=data.parent_id,
            is_active=data.is_active
        )
        db.add(category)
        db.commit()
        db.refresh(category)
        return category
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    


def get_categories(db: Session, page: int = 1, size: int = 10,filter:Optional[FilterCategory]=None) -> list[Categories]:
    try:
        query = db.query(Categories)
        if filter:
            if filter.search:
                # Use ilike for case-insensitive search
                search_term = f"%{filter.search}%"
                query = query.filter(
                    or_(
                        Categories.name_en.ilike(search_term),
                        Categories.name_ru.ilike(search_term),
                        Categories.name_uz.ilike(search_term),
                        Categories.description_en.ilike(search_term),
                        Categories.description_ru.ilike(search_term),
                        Categories.description_uz.ilike(search_term)
                    )
                )
            if  filter.is_active is not None:
                query = query.filter(Categories.is_active == filter.is_active)
            # if filter.parent_id:
            query = query.filter(Categories.parent_id == filter.parent_id)

            
        query = query.order_by(Categories.created_at.desc())
        total_count = query.count()
        categories = query.offset((page - 1) * size).limit(size).all()
        
        return {
            "items": categories,
            "total": total_count,
            "page": page,
            "size": size,
            'pages': (total_count + size - 1) // size 
        }
    except SQLAlchemyError as e:
        raise e
    

def get_category_by_id(db: Session, category_id: UUID) -> Optional[Categories]:
    try:
        return db.query(Categories).filter(Categories.id == category_id).first()
    except SQLAlchemyError as e:
        raise e 


def update_category(db: Session, category_id: UUID, data: UpdateCategory) -> Optional[Categories]:
    try:
        category = db.query(Categories).filter(Categories.id == category_id).first()
        if not category:
            return None
        
        for key, value in data.dict(exclude_unset=True).items():
            setattr(category, key, value)
        
        db.commit()
        db.refresh(category)
        return category
    except SQLAlchemyError as e:
        db.rollback()
        raise e

