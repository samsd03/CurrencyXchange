import sys
from django.shortcuts import render
from . import models
from django.http import JsonResponse
from CurrencyXchange.utils import decode_token,verify_currency_code
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_wallet(request):
    response = {"is_success" : False, "response_message" : "" ,"data":"","code" : 401}
    try:
        if request.method == "POST":
            token = request.headers['token']
            decode_data = decode_token(token)
            if decode_data:
                user_id = decode_data['user_id']
                postdata = request.POST
                currency_code = postdata.get('currency_code').upper()
                currency_quantity = postdata.get('currency_quantity')     
                if verify_currency_code(currency_code):                    
                    wallet_obj = models.UserWallet.objects.filter(user_id=user_id,currency_code=currency_code).first()
                    if not wallet_obj:
                        models.UserWallet.objects.create(user_id=user_id,currency_code=currency_code,currency_quantity=currency_quantity)
                        res_dict = {'is_success':True,'response_message':'Created Successfully','code':201}
                    else:
                        res_dict = {'response_message':'Currency Already Exist.Please Use Update Method to Update Currency','code':400}
                    response.update(res_dict)
                else:
                    response['response_message'] = "Invalid Currency Code"
            else:
                response['response_message'] = "Token Validation Error"
        else:
            response.update({'code':400,'response_message':'Method Not Allowed'})
    except Exception as e:
        response['response_message'] = 'Something Went Wrong'
        print(e," ERROR IN create_wallet --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    

    return JsonResponse(response)

@csrf_exempt
def update_wallet(request):
    response = {"is_success" : False, "response_message" : "" ,"data":"","code" : 401}
    try:
        if request.method == "POST":
            token = request.headers['token']
            decode_data = decode_token(token)
            if decode_data:
                user_id = decode_data['user_id']
                postdata = request.POST
                currency_code = postdata.get('currency_code').upper()
                currency_quantity = postdata.get('currency_quantity')
                if verify_currency_code(currency_code):                    
                    wallet_obj = models.UserWallet.objects.filter(user_id=user_id,currency_code=currency_code).first()
                    if wallet_obj:
                        total_quantity = wallet_obj.currency_quantity + int(currency_quantity)
                        
                        if total_quantity >= 0:
                            data_dict = {'total_quantity':total_quantity}
                            wallet_obj.currency_quantity = total_quantity
                            wallet_obj.save()                            
                            res_dict = {'is_success':True,'response_message':'Updated Successfully','code':204,'data':data_dict}
                        else:
                            data_dict = {'total_quantity':wallet_obj.currency_quantity}
                            res_dict = {'response_message':'Insufficient Quantity','code':400,'data':data_dict}
                    else:
                        res_dict = {'response_message':'Currency Does Not Exist.Please Use Create Method to Create Currency','code':400}
                    response.update(res_dict)
                else:
                    response['response_message'] = "Invalid Currency Code"
            else:
                response['response_message'] = "Token Validation Error"
        else:
            response.update({'code':400,'response_message':'Method Not Allowed'})
    except Exception as e:
        response['response_message'] = 'Something Went Wrong'
        print(e," ERROR IN update_wallet --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    

    return JsonResponse(response)

@csrf_exempt
def check_wallet(request):
    response = {"is_success" : False, "response_message" : "" ,"data":"","code" : 401}
    try:
        if request.method == "GET":
            token = request.headers['token']
            decode_data = decode_token(token)
            if decode_data:
                user_id = decode_data['user_id']
                user_wallet_obj = models.UserWallet.objects.filter(user_id=user_id)
                res_list = []
                for obj in user_wallet_obj:
                    currency_dict = {'currency_code':obj.currency_code,'currency_quantity':obj.currency_quantity}
                    res_list.append(currency_dict)
                res_dict = {'is_success':True,'response_message':'Listed Successfully','code':200,'data':res_list}
                response.update(res_dict)
            else:
                response['response_message'] = "Token Validation Error"
        else:
            response.update({'code':400,'response_message':'Method Not Allowed'})
    except Exception as e:
        response['response_message'] = 'Something Went Wrong'
        print(e," ERROR IN check_wallet --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    

    return JsonResponse(response)
