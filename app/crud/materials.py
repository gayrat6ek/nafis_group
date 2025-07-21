

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
from app.models.materials import Materials
from app.schemas.materials import CreateMaterials, UpdateMaterials


def create_material(db: Session, data: CreateMaterials) -> Materials:
    try:
        material = Materials(
            name_uz=data.name_uz,
            name_ru=data.name_ru,
            name_en=data.name_en,
            is_active=data.is_active
        )
        db.add(material)
        db.commit()
        db.refresh(material)
        return material
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def get_materials(db: Session, is_active: Optional[bool] = None, page: int = 1, size: int = 10,name: Optional[str] = None):
    try:
        query = db.query(Materials)
        if is_active is not None:
            query = query.filter(Materials.is_active == is_active)
        if name is not None:
            query = query.filter(or_(
                Materials.name_uz.ilike(f"%{name}%"),
                Materials.name_ru.ilike(f"%{name}%"),
                Materials.name_en.ilike(f"%{name}%")
            ))
        
        total_count = query.count()
        materials = query.offset((page - 1) * size).limit(size).all()
        return {
            "items": materials,
            "total": total_count,
            "page": page,
            "size": size,
            'pages': (total_count + size - 1) // size 
        }

        
    except SQLAlchemyError as e:
        raise e
    

def get_material_by_id(db: Session, material_id: UUID) -> Optional[Materials]:
    try:
        return db.query(Materials).filter(Materials.id == material_id).first()
    except SQLAlchemyError as e:
        raise e
    

def update_material(db: Session, material_id: UUID, data: UpdateMaterials) -> Optional[Materials]:
    try:
        material = db.query(Materials).filter(Materials.id == material_id).first()
        if not material:
            return None
        
        if data.name_uz is not None:
            material.name_uz = data.name_uz
        if data.name_ru is not None:
            material.name_ru = data.name_ru
        if data.name_en is not None:
            material.name_en = data.name_en
        if data.is_active is not None:
            material.is_active = data.is_active
        
        db.commit()
        db.refresh(material)
        return material
    except SQLAlchemyError as e:
        db.rollback()
        raise e