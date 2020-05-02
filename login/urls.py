from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^resgistration/$', views.resgistration , name="resgistration"),
]    