import jwt
import os
import sys

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
    except:
        print(e," ERROR IN decode_token --line number of error {}".format(sys.exc_info()[-1].tb_lineno))            
        return False