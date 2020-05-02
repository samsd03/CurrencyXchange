import jwt
import os
import sys
import json
import requests
from CurrencyXchange import constants

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
        print(e," ERROR IN decode_token --line number of error {}".format(sys.exc_info()[-1].tb_lineno))            
        return False

