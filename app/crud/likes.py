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
from app.models.likes import Likes
from app.schemas.likes import AddRemoveLike



def add_like(db: Session, data: AddRemoveLike,user_id) -> Likes:
    try:
        #check if the like already exists do not filter 

        existing_like = db.query(Likes).filter(
            Likes.product_id == data.product_id,
            Likes.user_id == user_id
        ).first()

        if existing_like:
            # If the like already exists, remove it
            db.delete(existing_like)
            db.commit()
            return None
        else:
            # If the like does not exist, create a new one
            new_like = Likes(
                product_id=data.product_id,
                user_id=user_id
            )
            db.add(new_like)
            db.commit()
            db.refresh(new_like)
            return new_like
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    
def count_likes(db: Session,user_id) -> int:
    try:
        count = db.query(Likes).filter(Likes.user_id==user_id).count()
        return count
    except SQLAlchemyError as e:
        raise e