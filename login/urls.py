from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^resgistration/$', views.resgistration , name="resgistration"),
    url(r'^login/$', views.login , name="login"),
    url(r'^upload_profile_picture/$', views.upload_profile_picture , name="upload_profile_picture"),

]    