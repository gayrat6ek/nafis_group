from app.db.session import SessionLocal
from typing import Union, Any,Optional
from datetime import datetime, timedelta
import pytz
from jose import jwt
from passlib.context import CryptContext
from openpyxl import load_workbook
import bcrypt
import random
import string


from sqlalchemy.orm import Session
from typing import Union, Any
from fastapi import (
    Depends,
    HTTPException,
    status,
)
import smtplib
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer
import xml.etree.ElementTree as ET
import os
#from schemas import user_schema
#from queries import user_query as crud
from dotenv import load_dotenv
from fastapi import (
    Depends,
    HTTPException,
    status,
)
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler

from app.db.session import SessionLocal
# from app.schemas.users import GetUserFullData
# from app.crud.users import get_user_by_username
from app.core.config import settings
from app.schemas.users import GetUserFullData
from app.crud.users import get_user_by_username



reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/api/v1/login", scheme_name="JWT")




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




async def get_current_user(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        expire_date = payload.get("exp")
        sub = payload.get("sub")
        permissions = payload.get('permissions')
        user = payload.get('user')
        if datetime.fromtimestamp(expire_date) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user["permissions"] = permissions

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    return user




class PermissionChecker:

    def __init__(self, required_permissions: str) -> None:
        self.required_permissions = required_permissions

    def __call__(self,user :dict = Depends(get_current_user)) -> dict:
        if self.required_permissions not in user['permissions']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to use this api",
            )
        return user






async def get_me(
    token: str = Depends(reuseable_oauth), db: Session = Depends(get_db)) -> GetUserFullData:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        expire_date = payload.get("exp")
        sub = payload.get("sub")
        if datetime.fromtimestamp(expire_date) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[dict[str, Any], None] = get_user_by_username(db=db, username=sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
