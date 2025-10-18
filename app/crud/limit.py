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
from app.models.limits import Limits
from app.schemas.limit import Limit


def create_or_update_limit(db: Session, limit: float) -> Limit:
    try:
        query = db.query(Limits).first()
        if query:
            query.limit = limit
            db.commit()
            db.refresh(query)
            return query
        else:
            query = Limits(limit=limit)
            db.add(query)
            db.commit()
            db.refresh(query)
            return query
    except SQLAlchemyError as e:
        raise e


def get_limit(db: Session) -> Limit:
    try:
        limit = db.query(Limits).first()
        return limit
    except SQLAlchemyError as e:
        raise e
    
