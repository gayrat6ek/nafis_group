from typing import List
from uuid import UUID
from fastapi import APIRouter
from fastapi import (
    Depends,
    HTTPException,
Security
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.crud import loanMonths as crud_loans_months
from app.routes.depth import get_db, PermissionChecker
from app.schemas.loanMonths import (
    LoanMonthsGet,
    LoanMonthsList,
    CreateLoanMonths,
    UpdateLoanMonths,)
from app.models.LoanMonths import LoanMonths
from app.utils.permissions import pages_and_permissions
loan_months_router = APIRouter()



@loan_months_router.get('/loan_months', response_model=List[LoanMonthsList])
async def get_loan_months_list(
        is_active: bool = None,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['LoanMonths']['view']))
):
    return crud_loans_months.get_loan_months(db=db, is_active=is_active)


@loan_months_router.get('/loan_months/{id}', response_model=LoanMonthsGet)
async def get_loan_months(
        id: UUID,
        db: Session = Depends(get_db),
        # current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['LoanMonths']['view']))
):
    loan_months = crud_loans_months.get_loan_months_by_id(db=db, loan_months_id=id)
    if not loan_months:
        raise HTTPException(status_code=404, detail="Loan months not found")
    return loan_months


@loan_months_router.post('/loan_months', response_model=LoanMonthsGet)
async def create_loan_months(
        body: CreateLoanMonths,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['LoanMonths']['create']))
):
    created_loan_months = crud_loans_months.create_loan_months(db=db, data=body)
    return created_loan_months


@loan_months_router.put('/loan_months/{id}', response_model=LoanMonthsGet)
async def update_loan_months(   
        id: UUID,
        body: UpdateLoanMonths,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['LoanMonths']['update']))
):
    updated_loan_months = crud_loans_months.update_loan_months(db=db, loan_months_id=id, data=body)
    if not updated_loan_months:
        raise HTTPException(status_code=404, detail="Loan months not found")
    return updated_loan_months