from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profit_loss_money_transfer/$', views.profit_loss_money_transfer , name="profit_loss_money_transfer"),
    url(r'^average_weekday_transfer/$', views.average_weekday_transfer , name="average_weekday_transfer"),
    
]   