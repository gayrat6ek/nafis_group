
from pickletools import read_unicodestringnl

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID

from app.models.LoanMonths import LoanMonths
from app.schemas.loanMonths import CreateLoanMonths, UpdateLoanMonths


def create_loan_months(db: Session, data: CreateLoanMonths) -> LoanMonths:
    try:
        loan_months = LoanMonths(
            months=data.months,
            percent=data.percent,
            description=data.description,
            is_active=data.is_active
        )
        db.add(loan_months)
        db.commit()
        db.refresh(loan_months)
        return loan_months
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    
def get_loan_months(db: Session,is_active: Optional[bool] = None,limit:Optional[int] = None):
    try:
        query = db.query(LoanMonths)
        if is_active is not None:
            query = query.filter(LoanMonths.is_active == is_active)
        query = query.order_by(LoanMonths.months.desc())
        
        if limit is not None:
            query = query.limit(limit)
        
        return query.all()
        
    except SQLAlchemyError as e:
        raise e
    


def get_loan_months_by_id(db: Session, loan_months_id: UUID) -> Optional[LoanMonths]:
    try:
        return db.query(LoanMonths).filter(LoanMonths.id == loan_months_id).first()
    except SQLAlchemyError as e:
        raise e
    

def update_loan_months(db: Session, loan_months_id: UUID, data: UpdateLoanMonths) -> Optional[LoanMonths]:
    try:
        loan_months = db.query(LoanMonths).filter(LoanMonths.id == loan_months_id).first()
        if not loan_months:
            return None
        
        if data.months is not None:
            loan_months.months = data.months
        if data.percent is not None:
            loan_months.percent = data.percent
        if data.description is not None:
            loan_months.description = data.description
        if data.is_active is not None:
            loan_months.is_active = data.is_active
        
        db.commit()
        db.refresh(loan_months)
        return loan_months
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    



    






