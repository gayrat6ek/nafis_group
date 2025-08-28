from email.contentmanager import raw_data_manager
import base64
from fastapi import APIRouter
from fastapi_pagination import paginate, Page,add_pagination
from typing import Optional
from uuid import UUID
from datetime import datetime, date
from typing import Annotated
from sqlalchemy.orm import Session
from app.crud import orders as orders_crud
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
    Header,
    Request,
    status,
)
from app.routes.depth import get_db, get_current_user
from app.schemas import users as user_sch
from app.crud.orders import getOrder,perform_transaction_orders
from app.crud import orders as orders_crud
from app.crud import orders as orders_crud
from app.crud.transactions import create_transaction_crud,filter_transactions,get_transaction_crud,update_transaction,get_transaction_with_transaction_id,get_transaction_with_order_id

import time
payme_route = APIRouter()


def generate_error_response(raw_body,code):
    return {
          "jsonrpc": "2.0",
          "id": raw_body['id'],
          "error": {
            "code": code,#-32504,
            "message": "We cannot perform such action"
          }
        }


def check_perform_transaction(db:Session,raw_data):
    order = getOrder(db=db,id = raw_data['params']['account']['order_id'])
    if not order:
        return generate_error_response(raw_data, -31099)
    if order.total_amount!=raw_data['params']['amount']:
        return generate_error_response(raw_data, -31001)

    return {
    "result" : {
        "allow" : True
    }
}


def create_transaction(db:Session,raw_data):
    order = getOrder(db=db, id=raw_data['params']['account']['order_id'])
    if not order:
        return generate_error_response(raw_data, -31099)


    transaction = get_transaction_with_transaction_id(db=db, id=raw_data['params']['id'])
    if transaction:
        return {
            "result": {
                'create_time': raw_data['params']['time'],
                'state': 1,
                'transaction': raw_data['params']['id'],

            }
        }

    order_transaction = get_transaction_with_order_id(db=db, id=raw_data['params']['account']['order_id'])

    if order_transaction:
        return generate_error_response(raw_data, -31099)

        # return generate_error_response(raw_data, -31050)




    created_query = create_transaction_crud(
        db=db,
        id=raw_data['id'],
        order_id=raw_data['params']['account']['order_id'],
        amount=raw_data['params']['amount'],
        time=raw_data['params']['time'],
        transaction_id=raw_data['params']['id'],
        )


    return {
        "result": {
            'create_time':raw_data['params']['time'],
            'state':1,
            'transaction':raw_data['params']['id'],

        }
    }

def perform_transaction(db:Session,raw_data):
    perform_time = int(time.time() * 1000)
    cancel_time =0
    order_transaction =get_transaction_with_transaction_id(db=db,id=raw_data['params']['id'])
    if order_transaction:
        if order_transaction.status!=1:
            return {
        "result":{
            'transaction':raw_data['params']['id'],
            'perform_time':order_transaction.perform_time,
            'state':order_transaction.status
        }
    }
    up_tr_q = update_transaction(db=db,id=raw_data['params']['id'],status=2,perform_time=perform_time,cancel_time=cancel_time,reason=None)
    perform_transaction_orders(db=db,order_id=up_tr_q.order_id)
    return {
        "result":{
            'transaction':raw_data['params']['id'],
            'perform_time':perform_time,
            'state':2
        }
    }

def cancel_transaction(db:Session,raw_data):

    cancel_time = int(time.time() * 1000)
    order_transaction = get_transaction_with_transaction_id(db=db, id=raw_data['params']['id'])
    if order_transaction:
        if order_transaction.status != 1:
            return {
                "result": {
                    'transaction': raw_data['params']['id'],
                    'cancel_time': order_transaction.cancel_time,
                    'state': order_transaction.status
                }
            }

    if raw_data['params']['reason']==3:
        status= -1
        perform_time = 0

    else:
        status=-2
        perform_time = int(time.time() * 1000)


    update_transaction(db=db, id=raw_data['params']['id'], status=status, perform_time=perform_time,cancel_time=cancel_time,reason=raw_data['params']['reason'])
    return {
        "result": {
            'transaction': raw_data['params']['id'],
            'cancel_time': cancel_time,
            'state':status

        }
    }

def check_transaction(db:Session,raw_data):
    transaction = get_transaction_with_transaction_id(db=db,id=raw_data['params']['id'])
    if transaction:
        return {
            'result':{
                'create_time':transaction.create_time,
                'perform_time':transaction.perform_time,
                'cancel_time':transaction.cancel_time,
                'transaction':transaction.transaction_id,
                'state':transaction.status,
                'reason':transaction.reason
            }
        }

    return generate_error_response(
        raw_data,
        -31003
    )



def get_statement(db:Session,raw_data):
    result = {
        'result':{
            'transactions':[

            ]
        }
    }
    transaction_list = filter_transactions(db=db,from_date=raw_data['params']['from'],to_date=raw_data['params']['to'])
    for transaction in transaction_list:
        curren_dict = {
            "id":transaction.id,
            'time':transaction.create_time,
            'amount':transaction.amount,
            'perform_time':transaction.perform_time,
            "create_time":transaction.create_time,
            'cancel_time':transaction.cancel_time,
            'transaction':transaction.transaction_id,
            'state':transaction.status,
            'reason':transaction.reason
        }

        result['result']['transactions'].append(curren_dict)
    return result




def check_authorization(auth_header: Optional[str]) -> bool:
    # Example login & password. Replace with your actual credentials or logic.
    expected_username = "Paycom"
    expected_password = "%FfiFIdxmFXRq?R&Rq5PNgSzVEVW#X6tuSOb"

    # 1. Check if header is provided
    if not auth_header:
        return False

    # 2. Check if header starts with "Basic "
    if not auth_header.startswith("Basic "):
        return False

    # 3. Decode Base64 portion
    #    - Remove the "Basic " prefix and decode what's left.
    encoded_credentials = auth_header.split("Basic ")[1].strip()
    try:
        decoded_bytes = base64.b64decode(encoded_credentials)
        decoded_str = decoded_bytes.decode("utf-8")  # Format: username:password

    except Exception:
        # Any error in decoding => invalid credentials
        return False

    # 4. Split username and password
    #    - Typically in Basic Auth: "username:password"
    if ":" not in decoded_str:
        return False

    username, password = decoded_str.split(":", 1)

    # 5. Compare with expected credentials
    if username == expected_username and password == expected_password:
        return True

    return False




@payme_route.post('/orders/transactions')
async def order_statuses(
        request:Request,
        db: Session = Depends(get_db),
):
    raw_body = await request.json()
    auth_header = request.headers.get("Authorization")
    checking_authorization = check_authorization(auth_header)
    if not checking_authorization:
        return generate_error_response(raw_body=raw_body,code=-32504)


    if raw_body['method']=='CheckPerformTransaction':
        return check_perform_transaction(db,raw_data=raw_body)


    if raw_body['method'] == 'CreateTransaction':
        return create_transaction(db,raw_data=raw_body)

    elif raw_body['method']=='PerformTransaction':
        return perform_transaction(db,raw_data=raw_body)

    elif raw_body['method']=='CancelTransaction':
        return cancel_transaction(db=db,raw_data=raw_body)

    elif raw_body['method']=='CheckTransaction':
        return check_transaction(db=db,raw_data=raw_body)

    elif raw_body['method']=='GetStatement':
        return  get_statement(db=db,raw_data=raw_body)

    else:
        return  generate_error_response(raw_body=raw_body,code='-32504')






@payme_route.post('/orders/statements')
async def order_statuses(
        request:Request,
        db: Session = Depends(get_db),
):
    data = filter_transactions(db=db,from_date=1734972088559,to_date=1734972088561)
    return data





