import json
import random
import string
from datetime import datetime, timedelta
from http.client import HTTPException
from typing import Union, Any
from jose import jwt
from typing import Optional
import bcrypt
import pytz
import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.base import JobLookupError, ConflictingIdError
from app.core.config import settings
from app.db.session import SessionLocal



timezonetash = pytz.timezone("Asia/Tashkent")
security = HTTPBasic()

def get_current_user_for_docs(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = settings.docs_username
    correct_password = settings.docs_password
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username



def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")



def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )




def create_access_token(subject: Union[str, Any], expires_delta: int = None,permissions:list=None,user_info:dict=None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode = {"exp": expires_delta, "sub": str(subject),"permissions":permissions,"user":user_info}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, settings.jwt_algorithm)
    return encoded_jwt



def create_refresh_token(subject: Union[str, Any], expires_delta: int = None,permissions:list=None,user_info:dict=None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.refresh_token_expire_minutes
        )

    to_encode = {"exp": expires_delta, "sub": str(subject),"permissions":permissions,"user":user_info}
    encoded_jwt = jwt.encode(to_encode, settings.jwt_refresh_secret_key, settings.jwt_algorithm)
    return encoded_jwt