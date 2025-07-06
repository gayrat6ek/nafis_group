from uuid import UUID
from fastapi import APIRouter
from fastapi_pagination import paginate, Page
from fastapi import (
    Depends,
    HTTPException,
Security
)

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.crud.users import get_user_by_username, get_user_list, createUserCrud,update_user, get_user_by_id
from app.routes.depth import get_db, get_current_user,PermissionChecker,get_me
from app.utils.permissions import pages_and_permissions
from app.schemas import users as user_sch
from app.utils.utils import verify_password, create_access_token, create_refresh_token,generateOtp

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


@user_router.post('/login')
async def login_user(
        form_data:user_sch.LoginClient,
        db: Session = Depends(get_db)
):
    user = get_user_by_username(db=db, username=form_data.username)

    if not user:
        raise HTTPException(status_code=404, detail="Invalid username")
    if not user.otp or user.otp != form_data.otp:
        raise HTTPException(status_code=404, detail="Invalid OTP")
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



@user_router.post("/users", )
async def create_user(
        user_data: user_sch.createUser,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Users']['create'])),
):
    if get_user_by_username(db=db, username=user_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user = createUserCrud(db=db, user=  user_data,otp=generateOtp(6))
    return {'success': True, 'message': 'User created successfully', 'id': str(user.id),'otp': user.otp}




@user_router.put("/users/{user_id}", response_model=user_sch.GetUserFullData)
async def update_user_data(
        user_id: str,
        user_data: user_sch.UpdateUser,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Users']['update'])),
):
    user_id = UUID(user_id)
    updated_user = update_user(db=db, user_id=user_id, user_data=user_data)
    
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return updated_user



@user_router.post("/users/{user_id}/otp", )
async def send_otp(
        user_id: str,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Users']['update'])),
):
    user_id = UUID(user_id)
    user = get_user_by_id(db=db, user_id=user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    otp = generateOtp(6)
    user.otp = otp
    db.commit()
    db.refresh(user)
    
    # Here you would typically send the OTP to the user's phone or email
    return {"success": True, "message": "OTP sent successfully", "otp": otp}






