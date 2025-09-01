

from pickletools import read_unicodestringnl

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

from app.models.Orders import Orders
import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID
from app.utils.utils import timezonetash
from app.models.OrderPaymentDates import OrderPaymentDates
from app.schemas.orderMonthlyPayment import OrderMonthlyPaymentUpdate

def checkIsalreadyCreated(db: Session, order_id: UUID):
    try:
        query = db.query(OrderPaymentDates).filter(OrderPaymentDates.order_id==order_id).first()
        if query:
            return True
        return False
    except SQLAlchemyError as e:
        raise e
def create_order_payment_date(db: Session, order_id: UUID, months, amount):
    if checkIsalreadyCreated(db,order_id):
        return True
    try:
        for i in range(months):
            payment_date = OrderPaymentDates(
                order_id=order_id,
                payment_date=datetime.now(tz=timezonetash) + timedelta(days=30 * (i + 1)),
                amount=amount
            )
            db.add(payment_date)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise e



def get_payment_dates_by_order_id(db: Session, order_id: Optional[UUID] = None, user_id: Optional[UUID] = None,is_paid: Optional[bool] = None):
    try:
        query =  db.query(OrderPaymentDates).join(OrderPaymentDates.order)
        if order_id is not None:
            query = query.filter(OrderPaymentDates.order_id == order_id)
        if user_id is not None:
            query = query.filter(Orders.user_id == user_id)
        if is_paid is not None:
            query = query.filter(OrderPaymentDates.is_paid == is_paid)
        query = query.order_by(OrderPaymentDates.payment_date.asc())
        return query.all()
    except SQLAlchemyError as e:
        raise e
    



def mark_as_paid(db:Session,payment_id:UUID):
    try:
        payment_date = db.query(OrderPaymentDates).filter(OrderPaymentDates.id == payment_id).first()
        if payment_date:
            payment_date.is_paid = True
            db.commit()
            db.refresh(payment_date)
            return payment_date
        return None
    except SQLAlchemyError as e:
        db.rollback()
        raise e