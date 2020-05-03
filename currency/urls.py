from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user_currency_conversion/$', views.user_currency_conversion , name="user_currency_conversion"),
    url(r'^user_currency_transfer/$', views.user_currency_transfer , name="user_currency_transfer"),

]   