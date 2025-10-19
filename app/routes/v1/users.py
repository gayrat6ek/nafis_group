from typing import Optional
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
from app.crud.users import get_user_by_username, get_user_list, createUserCrud,update_user, get_user_by_id,create_otp_verified_user,get_one_user
from app.routes.depth import get_db, get_current_user,PermissionChecker,get_me
from app.utils.permissions import pages_and_permissions
from app.schemas import users as user_sch
from app.utils.utils import verify_password, create_access_token, create_refresh_token,generateOtp,send_sms
from app.crud.otps import create_otp,check_otp
from app.crud.roles import get_role_by_name
from app.crud.likes import count_likes
from app.crud.limit import get_limit
from app.crud.orders import get_user_order_sum
from app.crud.orders import has_unpaid_order


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


@user_router.post('/client/login')
async def login_user(
        form_data:user_sch.LoginClient,
        db: Session = Depends(get_db)
):
    created = False
    user = get_user_by_username(db=db, username=form_data.username)

    if not user:
        if not check_otp(db=db, phone_number=form_data.username, otp_code=form_data.otp):
            raise HTTPException(status_code=404, detail="Invalid OTP")
        role = get_role_by_name(db=db, name='Clients')
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        
        user = create_otp_verified_user(db=db, username=form_data.username, otp=form_data.otp,role_id=role.id)
        created = True
        
        

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
        "refresh_token": create_refresh_token(subject=user.username, permissions=permissions, user_info=user_info),
        "created": created,
        "id": str(user.id),
    }


@user_router.get('/me', response_model=user_sch.GetUserFullData)
async def get_me(
        db: Session = Depends(get_db),
        current_user: user_sch.GetUserFullData = Depends(get_me)
):
    get_user = get_one_user(db=db, user_id=current_user.id)
    if get_user.limit_total is not None:
        limit = get_user.limit_total
    else:
        limit = get_limit(db=db)
        get_user.limit_total = limit.limit.limit
    likes = count_likes(db=db, user_id=current_user.id)
    orders_total = get_user_order_sum(db=db, user_id=current_user.id)
    limit_left = limit - orders_total
    # min left limit is 0
    
    current_user.limit_total = limit.limit
    current_user.like_count = int(likes)
    current_user.limit_left = max(0, limit_left)
    return current_user


@user_router.get("/users", response_model=Page[user_sch.GetUserFullData])
async def get_users(
        page: int = 1,
        size: int = 10,
        username: Optional[str]=None,
        full_name:Optional[str]=None,
        db: Session = Depends(get_db),
        current_user: dict= Depends(PermissionChecker(required_permissions=pages_and_permissions['Users']['view'])),
):
    return get_user_list(db=db, page=page, size=size,username=username,full_name=full_name)



@user_router.get("/users/{user_id}", response_model=user_sch.GetUserFullData)
async def get_user(
        user_id: str,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Users']['view'])),
):
    user_id = UUID(user_id)
    user = get_one_user(db=db, user_id=user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user



@user_router.post("/users")
async def create_user(
        user_data: user_sch.createUser,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Users']['create'])),
):
    if get_user_by_username(db=db, username=user_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user = createUserCrud(db=db, user=user_data,otp=generateOtp(6))
    return {'success': True, 'message': 'User created successfully', 'id': str(user.id),'otp': user.otp}







@user_router.put("/users/{user_id}", response_model=user_sch.GetUserFullData)
async def update_user_data(
        user_id: str,
        user_data: user_sch.UpdateUser,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Users']['update'])),
):
    user_id = UUID(user_id)
    current_user_data = get_one_user(db=db, user_id=user_id)
    if not current_user_data:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user_data.role.name != "Admin" and has_unpaid_order(db=db, user_id=current_user_data.id):
        raise HTTPException(status_code=400, detail="You have unpaid orders, you can't update your profile")
    
    if user_id == current_user['id'] and user_data.limit_total is not None:
        raise HTTPException(status_code=400, detail="You can't update your limit total")

    return update_user(db=db, user_id=user_id, user_data=user_data)


@user_router.post("/users/otp",)
async def send_otp(
        data: user_sch.SendOtpClient,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Users']['update'])),
):
    user = get_user_by_id(db=db, username=data.username)
    otp = generateOtp(6)
    
    if not user:
        create_otp(db=db, phone_number=data.username, otp_code=otp)
        send_sms(phone_number=data.username,otp=otp)
        return {"success": True, "message": "OTP sent successfully", "otp": otp}
    
    user.otp = otp
    db.commit()
    db.refresh(user)
    send_sms(phone_number=data.username,otp=otp)
    
    # Here you would typically send the OTP to the user's phone or email
    return {"success": True, "message": "OTP sent successfully", "otp": otp}






