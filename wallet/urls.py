from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create_wallet/$', views.create_wallet , name="create_wallet"),
    url(r'^update_wallet/$', views.update_wallet , name="update_wallet"),
    url(r'^check_wallet/$', views.check_wallet , name="check_wallet"),
]    