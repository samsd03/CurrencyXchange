import sys
from django.shortcuts import render
from CurrencyXchange.utils import decode_token
from django.views.decorators.csrf import csrf_exempt
from currency import models as currency_model
from django.http import JsonResponse
from currency.views import get_conversion_value

def find_profit_loss(user_id,currency,start_date,end_date):
    try:
        currency_current_price = {}
        currency_history_obj = currency_model.CurrencyTransferHistory.objects.filter(from_user_id=user_id,from_user_currency=currency)\
            .values('from_user_currency','from_user_quantity','to_user_currency','to_user_currency_price')
        if start_date:
            currency_history_obj = currency_history_obj.filter(event_time__date__gte=start_date)
        if end_date:
            currency_history_obj = currency_history_obj.filter(event_time__date__lte=end_date)
        total_count = len(currency_history_obj)
        total_profit_loss = 0
        for history in currency_history_obj:
            from_user_currency = history['from_user_currency']
            from_user_quantity = history['from_user_quantity']
            to_user_currency = history['to_user_currency']
            to_user_currency_price = history['to_user_currency_price']
            combine_currency = from_user_currency+'_'+to_user_currency
            if combine_currency not in currency_current_price:
                price = get_conversion_value(from_user_currency,from_user_quantity,to_user_currency)
                price_per_quantity = price['price_per_quantity']
                currency_current_price[combine_currency] = price_per_quantity
            else:
                price_per_quantity = currency_current_price[combine_currency]
            
            profit_loss = (float(price_per_quantity) - float(to_user_currency_price)) * float(from_user_quantity)
            total_profit_loss = profit_loss + total_profit_loss

        return round(total_profit_loss/total_count,2)

    except Exception as e:
        print(e," ERROR IN find_profit_loss --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    


@csrf_exempt
def profit_loss_money_transfer(request):
    response = {"is_success" : False, "response_message" : "" ,"data":"","code" : 401}
    try:
        if request.method == "POST":
            token = request.headers['token']
            decode_data = decode_token(token)
            if decode_data:
                user_id = decode_data['user_id']
                postdata = request.POST
                start_date = postdata.get('start_date')
                end_date = postdata.get('end_date')
                user_transfer_currency = currency_model.CurrencyTransferHistory.objects.filter(from_user_id=user_id)\
                    .values('from_user_currency').distinct()
                if start_date:
                    user_transfer_currency = user_transfer_currency.filter(event_time__date__gte=start_date)
                if end_date:
                    user_transfer_currency = user_transfer_currency.filter(event_time__date__lte=end_date)    
                profit_loss_dict = {}
                for unique_currency in user_transfer_currency:
                    from_currency = unique_currency['from_user_currency']
                    profit_loss = find_profit_loss(user_id,from_currency,start_date,end_date)
                    profit_loss_dict[from_currency] = profit_loss
                res_dict = {'is_success':True,'response_message':'Profit Loss Statement','code':200,'data':profit_loss_dict}
            else:
                response['response_message'] = "Token Validation Error"
            response.update(res_dict)
        else:
            response.update({'code':400,'response_message':'Method Not Allowed'})
    except Exception as e:
        response['response_message'] = 'Something Went Wrong'
        print(e," ERROR IN resgistration --line number of error {}".format(sys.exc_info()[-1].tb_lineno))    

    return JsonResponse(response)

