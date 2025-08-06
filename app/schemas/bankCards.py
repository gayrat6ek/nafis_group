
from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )   



class CreateBankCard(BaseConfig):
    card_number: str = Field(..., min_length=16, max_length=16, description="16-digit card number")
    cardholder_name: Optional[str] = Field(None, max_length=100, description="Name of the cardholder")
    expiration_date: str = Field(..., pattern=r"^(0[1-9]|1[0-2])/\d{2}$", description="Expiration date in MM/YY format")
    cvv: Optional[str] = Field(None, min_length=3, max_length=4, description="3 or 4-digit CVV code")
    is_active: bool = Field(default=True, description="Indicates if the card is active")
    card_phone_number: Optional[str] = Field(None, max_length=15, description="Phone number associated with the card, if applicable")
    user_id: UUID = Field(..., description="ID of the user to whom the card belongs")



class BankCardGet(BaseConfig):
    id: Optional[UUID] = None
    card_number: Optional[str] = None  # 16-digit card number
    cardholder_name: Optional[str] = None  # Name of the cardholder
    expiration_date: Optional[str] = None  # Expiration date in MM/YY format
    cvv: Optional[str] = None  # 3 or 4-digit CVV code
    is_active: Optional[bool] = True  # Indicates if the card is active
    card_phone_number: Optional[str] = None  # Phone number associated with the card, if applicable
    is_verified: Optional[bool] = False  # Indicates if the card is verified



class BankCardUpdate(BaseConfig):
    card_number: Optional[str] = Field(None, min_length=16, max_length=16, description="16-digit card number")
    cardholder_name: Optional[str] = Field(None, max_length=100, description="Name of the cardholder")
    expiration_date: Optional[str] = Field(None, pattern=r"^(0[1-9]|1[0-2])/\d{2}$", description="Expiration date in MM/YY format") 
    cvv: Optional[str] = Field(None, min_length=3, max_length=4, description="3 or 4-digit CVV code")
    is_active: Optional[bool] = Field(None, description="Indicates if the card is active")
    card_phone_number: Optional[str] = Field(None, max_length=15, description="Phone number associated with the card, if applicable")
    is_verified: Optional[bool] = Field(None, description="Indicates if the card is verified")
    
    # Note: user_id is not included in update schema as it should not be changed after creation
    # If needed, it can be added back with appropriate validation
