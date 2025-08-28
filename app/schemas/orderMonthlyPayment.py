
from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict



class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

class OrderMonthlyPaymentUpdate(BaseConfig):
    id: Optional[UUID] = None
    is_paid: Optional[bool] = False  # Indicates if the monthly payment is paid
    

class OrderMonthlyPaymentGet(BaseConfig):
    id: Optional[UUID] = None
    order_id: Optional[UUID] = None
    payment_date: Optional[datetime] = None
    amount: Optional[float] = None
    is_paid: Optional[bool] = False  # Indicates if the monthly payment is paid
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None