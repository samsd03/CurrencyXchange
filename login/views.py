import sys

from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate
from CurrencyXchange.utils import generate_token
from . import models
from CurrencyXchange.utils import decode_token

@csrf_exempt
def resgistration(request):
    response = {"is_success" : False, "response_message" : "" ,"data":"","code" : 401}
    try:
        if request.method == "POST":
            postdata = request.POST
            print(postdata)
            first_name = postdata.get("first_name")
            last_name = postdata.get("last_name")
            email = postdata.get("email")
            password = postdata.get("password")
            user_exist = User.objects.filter(username=email).first()
            if not user_exist:
                user = User.objects.create_user(username=email,email=email,first_name=first_name,\
                    last_name=last_name,password=password)        
                res_dict = {'is_success':True,'response_message':"User Registered Successfully",'code':201}
            else:
                res_dict = {'response_message':'User already exist with this email id'}
            response.update(res_dict)           
        else:
            response.update({'code':400,'response_message':'Method Not Allowed'})
    except Exception as e:
        response['response_message'] = 'Something Went Wrong'
        print(e," ERROR IN resgistration --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    

    return JsonResponse(response)

@csrf_exempt
def login(request):
    response = {"is_success" : False, "response_message" : "" ,"data":"","code" : 401}
    try:
        if request.method == "POST":
            postdata = request.POST
            email = postdata.get("email")
            password = postdata.get("password")
            user_obj = authenticate(username=email,password=password)
            if user_obj:
                user_id = user_obj.id
                token = generate_token(user_id)
                data = {'token':token}
                res_dict = {'is_success':True,'code':200,'response_message':"Login Successfully",'data':data}
            else:
                res_dict = {'response_message':"Login Failed"}
            response.update(res_dict)           
        else:
            response.update({'code':400,'response_message':'Method Not Allowed'})
    except Exception as e:
        response['response_message'] = 'Something Went Wrong'
        print(e," ERROR IN login --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    

    return JsonResponse(response)    

@csrf_exempt
def upload_profile_picture(request):
    response = {"is_success" : False, "response_message" : "" ,"data":"","code" : 401}
    try:
        if request.method == "POST":
            token = request.headers['token']
            decode_data = decode_token(token)
            if decode_data:
                user_id = decode_data['user_id']
                postdata = request.POST
                image = postdata.get("profile_picture")
                models.UserProfile.objects.create(user_id=user_id,profile_picture=image)
                res_dict = {'is_success':True,'response_message':"Profile Uploaded Successfully",'code':201}
                response.update(res_dict)
            else:
                response['response_message'] = "Token Validation Error"
        else:
            response.update({'code':400,'response_message':'Method Not Allowed'})
    except Exception as e:
        response['response_message'] = 'Something Went Wrong'
        print(e," ERROR IN upload_profile_picture --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    

    return JsonResponse(response)

