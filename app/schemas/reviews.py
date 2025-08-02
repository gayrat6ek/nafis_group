from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.users import GetUser

class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )   



class ReviewGet(BaseConfig):
    id: Optional[UUID] = None
    rating: Optional[int] = Field(..., ge=1, le=5, description="Rating of the product from 1 to 5")
    comment: Optional[str] = Field(None, max_length=500, description="Comment about the product")
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None
    images: Optional[List[str]] = Field(None, description="List of image URLs or paths associated with the review")
    user: Optional[GetUser] = None  # Assuming reviews are linked to users


class CreateReview(BaseConfig):
    product_id: UUID = Field(..., description="ID of the product being reviewed")
    rating: int = Field(..., ge=1, le=5, description="Rating of the product from 1 to 5")
    comment: Optional[str] = Field(None, max_length=500, description="Comment about the product")
    images: Optional[List[str]] = Field(None, description="List of image URLs or paths associated with the review")




class UpdateReview(BaseConfig):
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating of the product from 1 to 5")
    comment: Optional[str] = Field(None, max_length=500, description="Comment about the product")
    is_active: Optional[bool] = True
    images: Optional[List[str]] = Field(None, description="List of image URLs or paths associated with the review")
    answer: Optional[str] = Field(None, max_length=500, description="Answer to the review, if applicable")


