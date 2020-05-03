import sys
import requests
from CurrencyXchange.utils import decode_token,verify_currency_code
from CurrencyXchange import constants
from django.shortcuts import render
from wallet import models as wallet_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.models import User

# This will verify if user has sufficient amount of quantity of currency exist.
def check_user_balance(user_id,currency_code,currency_quantity):
    response = {'message':'','valid':False}
    try:
        user_wallet_obj = wallet_model.UserWallet.objects.filter(user_id=user_id,currency_code=currency_code).first()
        if user_wallet_obj:
            available_quantity = user_wallet_obj.currency_quantity
            if float(currency_quantity) <= float(available_quantity):
                response['valid'] = True
            else:
                response['message'] = "Insufficient quantity available for given currency"
        else:
            response['message'] = "Currency Does Not exist . Please Add currency first ."
                 
    except Exception as e:
        response['message'] = 'Something Went Wrong in check_user_balance'
        print(e," ERROR IN check_user_balance --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    

    return response

def transfer_convert_user_currency(to_user_id,add_currency_code,add_currency_quantity,from_user_id,reduce_currency_code,reduce_currency_quantity):
    status = False
    try:
        with transaction.atomic():
            user_wallet_obj = wallet_model.UserWallet.objects.filter(user_id=to_user_id,currency_code=add_currency_code).first()
            if user_wallet_obj:
                current_quantity = float(user_wallet_obj.currency_quantity)
                total_quantity = float(add_currency_quantity) + float(current_quantity)
                user_wallet_obj.currency_quantity = total_quantity
                user_wallet_obj.save()
            else:
                wallet_model.UserWallet.objects.create(user_id=to_user_id,currency_code=add_currency_code,currency_quantity=add_currency_quantity)
            user_wallet_reduce = wallet_model.UserWallet.objects.filter(user_id=from_user_id,currency_code=reduce_currency_code).first()
            if user_wallet_reduce:
                quantity = float(user_wallet_reduce.currency_quantity)
                total_quantity = float(quantity) - float(reduce_currency_quantity)
                user_wallet_reduce.currency_quantity = total_quantity
                user_wallet_reduce.save()
                status = True
            else:
                raise ValueError("Can not deduct amount from current in currency conversion")
    except Exception as e:
        status = False
        print(e," ERROR IN transfer_convert_user_currency --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    
    
    return status

def get_conversion_value(from_currency,from_quantity,to_currency):
    total_value_after_conversion = False
    try:
        conversion_url = constants.currency_conversion_url
        conversion_url = conversion_url.replace("FROM",from_currency.upper())
        conversion_url = conversion_url.replace("TO",to_currency.upper())
        print(conversion_url)
        conversion_request = requests.get(conversion_url)
        currency_data = conversion_request.json()
        from_currency_price = currency_data[from_currency+"_"+to_currency]
        total_value_after_conversion = round(float(from_quantity) * from_currency_price,2)
    except Exception as e:
        print(e," ERROR IN transfer_convert_user_currency --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    
    
    return total_value_after_conversion

@csrf_exempt
def user_currency_conversion(request):
    response = {"is_success" : False, "response_message" : "" ,"data":"","code" : 401}
    try:
        if request.method == "POST":
            token = request.headers['token']
            decode_data = decode_token(token)
            if decode_data:
                user_id = decode_data['user_id']
                postdata = request.POST
                from_currency = postdata.get('from_currency').upper()
                from_currency_quantity = postdata.get('from_currency_quantity').upper()
                to_currency = postdata.get('to_currency').upper()
                if verify_currency_code(from_currency) and verify_currency_code(to_currency):
                    quantity_validation = check_user_balance(user_id,from_currency,from_currency_quantity)
                    if quantity_validation['valid'] == True:
                        total_value_after_conversion  = get_conversion_value(from_currency,from_currency_quantity,to_currency)
                        if total_value_after_conversion:
                            conversion_status = transfer_convert_user_currency(user_id,to_currency,total_value_after_conversion,user_id,from_currency,from_currency_quantity)
                            if conversion_status:
                                res_dict = {'is_success':True,'response_message':'Converted Successfully','code':200}
                            else:
                                res_dict = {'response_message':'Conversion Error'}
                        else:
                            res_dict = {'response_message':'Error in conversion api'}
                        response.update(res_dict)
                    else:
                        response['response_message'] = quantity_validation['message']    
                else:
                    response['response_message'] = "Invalid From or To Currency Code"
            else:
                response['response_message'] = "Token Validation Error"
        else:
            response.update({'code':400,'response_message':'Method Not Allowed'})
    except Exception as e:
        response['response_message'] = 'Something Went Wrong'
        print(e," ERROR IN user_currency_conversion --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    

    return JsonResponse(response)

@csrf_exempt
def user_currency_transfer(request):
    response = {"is_success" : False, "response_message" : "" ,"data":"","code" : 401}
    try:
        if request.method == "POST":
            token = request.headers['token']
            decode_data = decode_token(token)
            if decode_data:
                user_id = decode_data['user_id']
                postdata = request.POST
                from_user_currency = postdata.get('from_user_currency').upper()
                from_user_currency_quantity = postdata.get('from_user_currency_quantity')
                to_user_id = postdata.get('to_user_id')
                to_user_currency = postdata.get('to_user_currency').upper()
                if verify_currency_code(from_user_currency) and verify_currency_code(to_user_currency):
                    quantity_validation = check_user_balance(user_id,from_user_currency,from_user_currency_quantity)
                    if quantity_validation['valid'] == True:
                        to_user_obj = User.objects.filter(id=to_user_id).first()
                        if to_user_obj:
                            total_value_after_conversion  = get_conversion_value(from_user_currency,from_user_currency_quantity,to_user_currency)                            
                            if total_value_after_conversion:
                                transfer_status = transfer_convert_user_currency(to_user_id,to_user_currency,total_value_after_conversion,user_id,from_user_currency,from_user_currency_quantity)
                                if transfer_status:
                                    res_dict = {'is_success':True,'response_message':'Transferred Successfully','code':200}
                                else:
                                    res_dict = {'response_message':'Transfer Falied'}                                
                            else:
                                res_dict = {'response_message':'Error in conversion api'}
                            response.update(res_dict)
                        else:
                            response['response_message'] = "To User Not Found"
                    else:
                        response['response_message'] = quantity_validation['message']
                else:
                    response['response_message'] = "Invalid From or To Currency Code"
            else:
                response['response_message'] = "Token Validation Error"
    except Exception as e:
        response['response_message'] = 'Something Went Wrong'
        print(e," ERROR IN user_currency_transfer --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    

    return JsonResponse(response)
