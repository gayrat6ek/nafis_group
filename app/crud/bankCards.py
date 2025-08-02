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


from app.models.bank_cards import BankCards
from app.schemas.bankCards import CreateBankCard, BankCardUpdate




def create_bank_card(db: Session, data: CreateBankCard) -> BankCards:
    try:
        bank_card = BankCards(
            user_id=data.user_id,
            card_number=data.card_number,
            cardholder_name=data.cardholder_name,
            expiration_date=data.expiration_date,
            cvv=data.cvv,
            is_active=True,
            card_phone_number=data.card_phone_number,
            is_verified=False # Initially set to False, can be updated after verification
        )
        db.add(bank_card)
        db.commit()
        db.refresh(bank_card)
        return bank_card
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    


def update_bank_card(db: Session, card_id: UUID, data: BankCardUpdate) -> Optional[BankCards]:
    try:
        bank_card = db.query(BankCards).filter(BankCards.id == card_id).first()
        if not bank_card:
            return None
        
        if data.card_number is not None:
            bank_card.card_number = data.card_number
        if data.cardholder_name is not None:
            bank_card.cardholder_name = data.cardholder_name
        if data.expiration_date is not None:
            bank_card.expiration_date = data.expiration_date
        if data.cvv is not None:
            bank_card.cvv = data.cvv
        if data.is_active is not None:
            bank_card.is_active = data.is_active
        if data.card_phone_number is not None:
            bank_card.card_phone_number = data.card_phone_number
        if data.is_verified is not None:
            bank_card.is_verified = data.is_verified
        
        db.commit()
        db.refresh(bank_card)
        return bank_card
    except SQLAlchemyError as e:
        db.rollback()
        raise e 
    


def get_bank_cards(db: Session, user_id: UUID, is_active: Optional[bool] = None):
    try:
        query = db.query(BankCards).filter(BankCards.user_id == user_id)
        
        if is_active is not None:
            query = query.filter(BankCards.is_active == is_active)
        
        bank_cards = query.all()
        return bank_cards
    except SQLAlchemyError as e:
        raise e