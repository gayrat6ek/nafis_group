
from app.utils.utils import hash_password
from app.models.Users import Users
from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID
from app.schemas.users import createUser, UpdateUser


def create_user(db:Session,username,fullname,password,role_id):
    query = Users(
        username=username,
        full_name=fullname,
        password=hash_password(password),
        role_id=role_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return  query


def get_user_by_username(db:Session,username):
    query = db.query(Users).filter(Users.username==username).first()
    return query


def get_user_list(db:Session, page: int = 1, size: int = 10):
    query = db.query(Users)
    total_count = query.count()
    users = query.offset((page - 1) * size).limit(size).all()
    
    return {
        "items": users,
        "total": total_count,
        "page": page,
        "size": size,
        'pages': (total_count + size - 1) // size 
    }



def create_client(db:Session,username,full_name):
    query = Users(username=username,full_name=full_name)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query




def update_user(db:Session, user_id: UUID, user_data: UpdateUser):
    query = db.query(Users).filter(Users.id == user_id).first()
    if not query:
        return None
    
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(query, key, value)
    
    db.commit()
    db.refresh(query)
    return query



def get_user_by_id(db: Session, user_id: UUID):
    query = db.query(Users).filter(Users.id == user_id).first()
    return query

def createUserCrud(db: Session, user: createUser,otp):
    hashed_password = hash_password(user.password)
    new_user = Users(
        username=user.username,
        full_name=user.full_name,
        password=hashed_password,
        role_id=user.role_id,
        is_client=user.is_client,
        otp=otp,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user