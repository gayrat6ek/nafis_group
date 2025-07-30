

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
from app.models.pickUpLocations import PickUpLocations
from app.schemas.pickUpLocations import PickUpLocationCreate,PickUpLocationUpdate



def createUpLocations(db:Session,data:PickUpLocationCreate):
    try:
        new_location = PickUpLocations(
            name_uz=data.name_uz,
            name_ru=data.name_ru,
            name_en=data.name_en,
            address=data.address,
            is_active=data.is_active,
            lat=data.lat,
            lon=data.lon
        )
        db.add(new_location)
        db.commit()
        db.refresh(new_location)
        return new_location
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    


def updateUpLocations(db:Session,location_id:UUID,data:PickUpLocationUpdate):
    try:
        location = db.query(PickUpLocations).filter(PickUpLocations.id == location_id).first()
        if not location:
            return None
        
        if data.name_uz is not None:
            location.name_uz = data.name_uz
        if data.name_ru is not None:
            location.name_ru = data.name_ru
        if data.name_en is not None:
            location.name_en = data.name_en
        if data.address is not None:
            location.address = data.address
        if data.is_active is not None:
            location.is_active = data.is_active
        if data.lat is not None:
            location.lat = data.lat
        if data.lon is not None:
            location.lon = data.lon
        
        db.commit()
        db.refresh(location)
        return location
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def getUpLocations(db:Session,is_active:Optional[bool]=None):
    try:
        query = db.query(PickUpLocations)
        if is_active is not None:
            query = query.filter(PickUpLocations.is_active == is_active)
        return query.all()
    except SQLAlchemyError as e:
        raise e
    

def getUpLocationById(db:Session,location_id:UUID):
    try:
        location = db.query(PickUpLocations).filter(PickUpLocations.id == location_id).first()
        return location
    except SQLAlchemyError as e:
        raise e