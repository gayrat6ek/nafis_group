

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

from app.models.measureUnits import MeasureUnits
from app.schemas.measureUnits import CreateMeasureUnits, UpdateMeasureUnits



def create_measure_unit(db: Session, data: CreateMeasureUnits) -> MeasureUnits:
    try:
        measure_unit = MeasureUnits(
            title_uz=data.title_uz,
            title_ru=data.title_ru,
            title_en=data.title_en,
            name_uz=data.name_uz,
            name_ru=data.name_ru,
            name_en=data.name_en,
            is_active=data.is_active
        )
        db.add(measure_unit)
        db.commit()
        db.refresh(measure_unit)
        return measure_unit
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    


def get_measure_units(db: Session, is_active: Optional[bool] = None):
    try:
        query = db.query(MeasureUnits)
        if is_active is not None:
            query = query.filter(MeasureUnits.is_active == is_active)
        
        return query.all()
        
    except SQLAlchemyError as e:
        raise e
    

def get_measure_unit_by_id(db: Session, measure_unit_id: UUID) -> Optional[MeasureUnits]:
    try:
        return db.query(MeasureUnits).filter(MeasureUnits.id == measure_unit_id).first()
    except SQLAlchemyError as e:
        raise e
    


def update_measure_unit(db: Session, measure_unit_id: UUID, data: UpdateMeasureUnits) -> Optional[MeasureUnits]:
    try:
        measure_unit = db.query(MeasureUnits).filter(MeasureUnits.id == measure_unit_id).first()
        if not measure_unit:
            return None
        
        if data.name_uz is not None:
            measure_unit.name_uz = data.name_uz
        if data.name_ru is not None:
            measure_unit.name_ru = data.name_ru
        if data.name_en is not None:
            measure_unit.name_en = data.name_en
        if data.is_active is not None:
            measure_unit.is_active = data.is_active
        if data.title_uz is not None:
            measure_unit.title_uz = data.title_uz
        if data.title_ru is not None:
            measure_unit.title_ru = data.title_ru
        if data.title_en is not None:
            measure_unit.title_en = data.title_en
        
        db.commit()
        db.refresh(measure_unit)
        return measure_unit
    except SQLAlchemyError as e:
        db.rollback()
        raise e