

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
from app.models.otps import Otps


def create_otp(db: Session, phone_number: str, otp_code: str) -> Otps:
    try:
        otp = Otps(
            phone_number=phone_number,
            otp_code=otp_code,
            is_verified=False
        )
        db.add(otp)
        db.commit()
        db.refresh(otp)
        return otp
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    

def check_otp(db: Session, phone_number: str, otp_code: str) -> Optional[Otps]:
    try:
        otp = db.query(Otps).filter(
            Otps.phone_number == phone_number,
            Otps.otp_code == otp_code,
        ).first()
        return otp
    except SQLAlchemyError as e:
        raise e