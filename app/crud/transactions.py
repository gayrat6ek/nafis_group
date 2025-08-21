from sqlalchemy.orm import Session
from typing import Optional
import bcrypt
import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID
from app.models.transactions import Transactions


def create_transaction_crud(db:Session,id,order_id,amount,time,transaction_id):
    query = Transactions(
        id=id,
        order_id=order_id,
        amount=amount,
        create_time=time,
        transaction_id=transaction_id,
        status=1
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def update_transaction(db:Session,id,status,perform_time,cancel_time,reason):
    query = db.query(Transactions).filter(Transactions.transaction_id==id).first()
    if query:
        query.status=status
        query.perform_time=perform_time
        query.cancel_time=cancel_time
        query.reason=reason
        db.commit()
        db.refresh(query)
    return query


def filter_transactions(db:Session,from_date,to_date):
    query = db.query(Transactions).filter( and_(
        Transactions.create_time >=from_date,
        Transactions.create_time <= to_date
    )).all()
    return query



def get_transaction_crud(db:Session,id):
    query = db.query(Transactions).filter(Transactions.id==id).first()
    return query


def get_transaction_with_transaction_id(db:Session,id):
    query = db.query(Transactions).filter(Transactions.transaction_id==id).first()
    return query


def get_transaction_with_order_id(db:Session,id):
    query = db.query(Transactions).filter(Transactions.order_id==id,Transactions.status==1).first()
    return query

