import jwt
import os
import sys
import json
import requests
import datetime
from CurrencyXchange.generate_order_pdf import order_inv
from CurrencyXchange import constants
from currency.models import CurrencyTransferHistory

SECRET_KEY = os.environ.get('secret_key')

def generate_token(user_id):
    try:
        data = {'user_id': str(user_id)}
        encoded_token = jwt.encode(data ,SECRET_KEY ,algorithm='HS256' ).decode('utf-8')
        return encoded_token
    except Exception as e:
        print(e," ERROR IN generate_token --line number of error {}".format(sys.exc_info()[-1].tb_lineno))            
        return False

def decode_token(token):
    try:
        decoded_data =  jwt.decode(token,SECRET_KEY,algorithm='HS256')
        return decoded_data
    except Exception as e:
        print(e," ERROR IN decode_token --line number of error {}".format(sys.exc_info()[-1].tb_lineno))            
        return False

def verify_currency_code(currency_code):
    try:
        verify_currency_url = constants.currency_code_verify_url.replace('replace_code_here',currency_code)
        verify_currency_request = requests.get(verify_currency_url)        
        if verify_currency_request.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print(e," ERROR IN verify_currency_code --line number of error {}".format(sys.exc_info()[-1].tb_lineno))            
        return False
#order_id,date,name,from_currency,from_currency_quantity,to_currency
def generate_order_invoice(order_id):
    try:
        print(order_id)
        transfer_obj = CurrencyTransferHistory.objects.get(id=order_id)
        name = transfer_obj.to_user.get_full_name()
        print(name)
        from_currency = transfer_obj.from_user_currency
        from_currency_quantity = transfer_obj.from_user_quantity
        to_currency = transfer_obj.to_user_currency
        current_time = datetime.datetime.now() 
        invoice_path = order_inv(order_id,current_time,name,from_currency,from_currency_quantity,to_currency)

    except Exception as e:
        print(e," ERROR IN generate_order_invoice --line number of error {}".format(sys.exc_info()[-1].tb_lineno))            
        return False
