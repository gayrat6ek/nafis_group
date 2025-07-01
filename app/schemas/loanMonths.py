
from datetime import datetime
from symtable import Class
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class BaseConfig(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )


class LoanMonthsGet(BaseConfig):
    id: Optional[UUID] = None
    months: Optional[int] = None
    percent: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None

class LoanMonthsList(BaseConfig):
    id: UUID
    months: Optional[int] = None
    percent: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = None

class CreateLoanMonths(BaseConfig):
    months: int
    percent: float
    description: Optional[str] = None
    is_active: Optional[bool] = True

class UpdateLoanMonths(BaseConfig):
    months: Optional[int] = None
    percent: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True