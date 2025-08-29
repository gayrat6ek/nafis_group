from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter
from fastapi import (
    Depends,
    HTTPException,
Security
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_pagination import Page
from sqlalchemy.orm import Session


from app.routes.depth import get_db, PermissionChecker
from app.crud import orderPaymentDates as crud_order_monthly_payment
from app.schemas.orderMonthlyPayment import (
    OrderMonthlyPaymentGet,OrderMonthlyPaymentUpdate)
from app.utils.permissions import pages_and_permissions



app_monthly_payment_router = APIRouter()


@app_monthly_payment_router.get('/order_monthly_payments', response_model=List[OrderMonthlyPaymentGet])
async def get_order_monthly_payment( 
        order_id: Optional[UUID] = None,
        is_paid: bool = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['view']))
):
    order_monthly_payment = crud_order_monthly_payment.get_payment_dates_by_order_id(db=db, order_id=order_id, user_id=current_user['id'], is_paid=is_paid)
    return order_monthly_payment




@app_monthly_payment_router.get('/admin/order_monthly_payments', response_model=List[OrderMonthlyPaymentGet])
async def get_order_monthly_payment( 
        order_id: UUID,
        user_id: UUID = None,
        is_paid: bool = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']['admin_view']))
):
    order_monthly_payment = crud_order_monthly_payment.get_payment_dates_by_order_id(db=db, order_id=order_id, user_id=user_id, is_paid=is_paid)
    return order_monthly_payment


@app_monthly_payment_router.put('/mark_as_paid/{payment_id}',)
async def update_order_monthly_payment(  
        payment_id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['Orders']["admin_update_order"]))
):
    updated_order_monthly_payment = crud_order_monthly_payment.mark_as_paid(db=db, payment_id=payment_id)
    if not updated_order_monthly_payment:
        raise HTTPException(status_code=404, detail="Order monthly payment not found")
    return updated_order_monthly_payment