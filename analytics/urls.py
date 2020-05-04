from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profit_loss_money_transfer/$', views.profit_loss_money_transfer , name="profit_loss_money_transfer"),

]   