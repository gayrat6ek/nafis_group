
from typing import List
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
from app.crud import bankCards as crud_bank_cards
from app.routes.depth import get_db, PermissionChecker
from app.schemas.bankCards import (
    CreateBankCard,
    BankCardUpdate,
    BankCardGet,
)
from app.utils.permissions import pages_and_permissions
from app.crud.orders import has_unpaid_order

bank_cards_router = APIRouter()



@bank_cards_router.get('/bank_cards', response_model=List[BankCardGet])
async def get_bank_cards_list(
        user_id: UUID,
        is_active: bool = None,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['BankCards']['view']))
):
    return crud_bank_cards.get_bank_cards(db=db, user_id=user_id, is_active=is_active)


@bank_cards_router.get('/bank_cards/{id}', response_model=BankCardGet)
async def get_bank_card(
        id: UUID,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['BankCards']['view']))
):
    bank_card = crud_bank_cards.get_bank_card_by_id(db=db, card_id=id)
    if not bank_card:
        raise HTTPException(status_code=404, detail="Bank card not found")
    return bank_card


@bank_cards_router.post('/bank_cards', response_model=BankCardGet)
async def create_bank_card(
        body: CreateBankCard,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['BankCards']['create']))
):
    if body.user_id is None:
        body.user_id = current_user['id']
    created_bank_card = crud_bank_cards.create_bank_card(db=db, data=body)
    return created_bank_card


@bank_cards_router.put('/bank_cards/{id}', response_model=BankCardGet)
async def update_bank_card(
        id: UUID,
        body: BankCardUpdate,
        db: Session = Depends(get_db),
        current_user: dict = Depends(PermissionChecker(required_permissions=pages_and_permissions['BankCards']['update']))
):
    if has_unpaid_order(db=db, user_id=current_user['id']):
        raise HTTPException(status_code=400, detail="You have unpaid orders, you can't update your bank card")
    updated_bank_card = crud_bank_cards.update_bank_card(db=db, card_id=id, data=body)
    if not updated_bank_card:
        raise HTTPException(status_code=404, detail="Bank card not found")
    return updated_bank_card