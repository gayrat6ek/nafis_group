
from curses import noecho
from app.utils.utils import hash_password, timezonetash
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


def get_user_list(db:Session,username:Optional[str]=None,full_name:Optional[str]=None, page: int = 1, size: int = 10,):
    query = db.query(Users)
    if username is not None:
        query = query.filter(Users.username.ilike(f"%{username}%"))
    if full_name is not None:
        query = query.filter(Users.full_name.ilike(f"%{full_name}%"))
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
    
    if user_data.birth_date is not None:
        query.birth_date = user_data.birth_date
    if user_data.full_name is not None:
        query.full_name = user_data.full_name
    if user_data.username is not None:
        query.username = user_data.username
    if user_data.role_id is not None:
        query.role_id = user_data.role_id
    if user_data.is_client is not None:
        query.is_client = user_data.is_client
    if user_data.passport_front_image is not None:
        query.passport_front_image = user_data.passport_front_image
    if user_data.passport_back_image is not None:
        query.passport_back_image = user_data.passport_back_image
    if user_data.person_passport_image is not None:
        query.person_passport_image = user_data.person_passport_image
    if user_data.passport_series is not None:
        query.passport_series = user_data.passport_series
    if user_data.extra_phone_number is not None:
        query.extra_phone_number = user_data.extra_phone_number
    if user_data.email is not None:
        query.email = user_data.email
    if user_data.is_verified is not None:
        query.is_verified = user_data.is_verified
    if user_data.is_active is not None:
        query.is_active = user_data.is_active
    if user_data.marriage_status is not None:
        query.marriage_status = user_data.marriage_status
    if user_data.job is not None:
        query.job = user_data.job
    if user_data.salary is not None:
        query.salary = user_data.salary
    if user_data.exerience is not None:
        query.exerience = user_data.exerience
    if user_data.limit_total is not None:
        query.limit_total = user_data.limit_total
    if user_data.black_list_reason is not None:
        query.black_list_reason = user_data.black_list_reason
    if user_data.black_list_days is not None:
        query.black_list_date = datetime.now(tz=timezonetash) + timedelta(days=int(user_data.black_list_days))

    db.commit()
    db.refresh(query)
    return query



def get_user_by_id(db: Session, username):
    query = db.query(Users).filter(Users.username == username).first()
    return query




def createUserCrud(db: Session, user: createUser,otp):
    if user.password is not None:
        user.password = hash_password(user.password)
    

    new_user = Users(
        username=user.username,
        full_name=user.full_name,
        password=user.password,
        role_id=user.role_id,
        is_client=user.is_client,
        otp=otp,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_otp_verified_user(db:Session,username,otp,role_id: Optional[UUID] = None):
    query = Users(
        username=username,
        otp=otp,
        role_id=role_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def get_one_user(db: Session, user_id: UUID):
    query = db.query(Users).filter(Users.id == user_id).first()
    return query