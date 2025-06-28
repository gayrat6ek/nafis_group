from fastapi import APIRouter
from fastapi_pagination import paginate, Page
from fastapi import (
    Depends,
    HTTPException,
Security
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.crud.users import get_user_by_username, get_user_list
from app.routes.depth import get_db, get_current_user,PermissionChecker,get_me
from app.utils.permissions import pages_and_permissions
from app.schemas import users as user_sch
from app.utils.utils import verify_password, create_access_token, create_refresh_token

user_router = APIRouter()


@user_router.post('/login')
async def login_user(
        form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
        db: Session = Depends(get_db)
):
    user = get_user_by_username(db=db, username=form_data.username)

    if not user:
        raise HTTPException(status_code=404, detail="Invalid username")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=404, detail="Invalid password")
    permissions = user.role.permissions if user.role else []
    user_info = {
        "id": str(user.id),
        "username": user.username,
        "fullname": user.full_name
    }

    return {
        "access_token": create_access_token(subject=user.username, permissions=permissions, user_info=user_info),
        "refresh_token": create_refresh_token(subject=user.username, permissions=permissions, user_info=user_info)
    }


@user_router.get('/me', response_model=user_sch.GetUserFullData)
async def get_me(
        db: Session = Depends(get_db),
        current_user: user_sch.GetUserFullData = Depends(get_me)
):
    return current_user


@user_router.get("/users", response_model=user_sch.GetUserFullData)
async def get_users(
        page: int = 1,
        size: int = 10,
        db: Session = Depends(get_db),
        current_user: dict= Depends(PermissionChecker(required_permissions=pages_and_permissions['Users']['view'])),
):
    return get_user_list(db=db, page=page, size=size)
