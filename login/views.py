from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

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
            user = User.objects.create_user(username=email,email=email,first_name=first_name,\
                   last_name=last_name,password=password)        
            res_dict = {'is_success':True,'response_message':"User Registered Successfully",'code':201}
            response.update(res_dict)           
        else:
            response.update({'code':400,'response_message':'Method Not Allowed'})
    except Exception as e:
        response['response_message'] = 'Something Went Wrong'
        print(e," ERROR IN resgistration --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    

    return JsonResponse(response)

    
