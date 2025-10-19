from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.roles import RolesGet



# class GetUserFullData(BaseModel):
#     id:Optional[UUID]=None
#     full_name: Optional[str]=None
#     username:Optional[str]=None
#     created_at:Optional[datetime]=None
#     role:Optional[RolesGet]=None
#     model_config = ConfigDict(
#         from_attributes=True
#     )



class GetUser(BaseModel):
    id:Optional[UUID]=None
    full_name: Optional[str]=None
    username:Optional[str]=None
    model_config = ConfigDict(
        from_attributes=True
    )



class createUser(BaseModel):
    #username as phone number like 998901234567
    username: str = Field(..., min_length=12, max_length=12, pattern=r'^\d{12}$', description="Phone number in format 998901234567")
    full_name: Optional[str] = Field(None, description="Full name of the user")
    password: Optional[str] = Field(None, min_length=6, description="Password for the user")
    role_id: Optional[UUID] = Field(None, description="Role ID of the user")
    is_client: Optional[bool] = Field(True, description="Indicates if the user is a client")



class UpdateUser(BaseModel):
    full_name: Optional[str] = Field(None, description="Full name of the user")
    username: Optional[str] = Field(None, min_length=12, max_length=12, pattern=r'^\d{12}$', description="Phone number in format 998901234567")
    role_id: Optional[UUID] = Field(None, description="Role ID of the user")
    is_client: Optional[bool] = Field(True, description="Indicates if the user is a client")
    passport_front_image: Optional[str] = Field(None, description="Passport front image URL")
    passport_back_image: Optional[str] = Field(None, description="Passport back image URL")
    person_passport_image: Optional[str] = Field(None, description="Person passport image URL")
    passport_series: Optional[str] = Field(None, description="Passport series")
    extra_phone_number: Optional[str] = Field(None, description="Extra phone number of the user")
    birth_date: Optional[datetime] = Field(None, description="Birth date of the user")
    email: Optional[str] = Field(None, description="Email of the user")
    is_verified: Optional[bool] = Field(False, description="Indicates if the user is verified")
    is_active: Optional[bool] = Field(True, description="Indicates if the user is active")
    marriage_status: Optional[str] = Field(None, description="Marriage status of the user")
    job: Optional[str] = Field(None, description="Job of the user")
    salary: Optional[str] = Field(None, description="Salary of the user")
    exerience: Optional[float] = Field(None, description="Work experience of the user in years")
    limit_total: Optional[float] = Field(None, description="Limit total of the user")


class GetUserFullData(BaseModel):
    id: UUID
    full_name: Optional[str] = None
    username: Optional[str] = None
    role_id: Optional[UUID] = None
    is_client: Optional[bool] = True
    passport_front_image: Optional[str] = None
    passport_back_image: Optional[str] = None
    person_passport_image: Optional[str] = None
    passport_series: Optional[str] = None
    extra_phone_number: Optional[str] = None
    birth_date: Optional[datetime] = None
    email: Optional[str] = None
    is_verified: Optional[bool] = False
    is_active: Optional[bool] = True
    created_at: datetime
    updated_at: Optional[datetime] = None
    marriage_status: Optional[str] = None
    job: Optional[str] = None
    salary: Optional[str] = None
    exerience: Optional[float] = None
    role : Optional[RolesGet] = None
    like_count: Optional[int] = 0  # Assuming this is the count of likes for the user
    limit_total: Optional[float] = 0
    limit_left: Optional[float]= 0

    model_config = ConfigDict(
        from_attributes=True
    )


class GetUserFullDataInOrder(BaseModel):
    id: UUID
    full_name: Optional[str] = None
    username: Optional[str] = None
    is_client: Optional[bool] = True
    passport_front_image: Optional[str] = None
    passport_back_image: Optional[str] = None
    person_passport_image: Optional[str] = None
    passport_series: Optional[str] = None
    extra_phone_number: Optional[str] = None
    birth_date: Optional[datetime] = None
    is_verified: Optional[bool] = False
    is_active: Optional[bool] = True
    marriage_status: Optional[str] = None
    job: Optional[str] = None
    salary: Optional[str] = None
    exerience: Optional[float] = None

    model_config = ConfigDict(
        from_attributes=True
    )


class LoginClient(BaseModel):
    username: str = Field(..., min_length=12, max_length=12, pattern=r'^\d{12}$', description="Phone number in format 998901234567")
    otp: Optional[str] = Field(None, description="One Time Password for the user")

    model_config = ConfigDict(
        from_attributes=True
    )


class SendOtpClient(BaseModel):
    username: str = Field(..., min_length=12, max_length=12, pattern=r'^\d{12}$', description="Phone number in format 998901234567")

    model_config = ConfigDict(
        from_attributes=True
    )