from django.urls import path
from django.urls import include, re_path as url
from . import views

urlpatterns = [
	url(r'^v1/logout$', views.user_logout, name="user_logout"),
	url(r'^v1/web/login$', views.web_login, name="web_login"),
	url(r'^loginuser$', views.login_me, name="login_me"),
	url(r'^update/notification/token$', views.update_notification_token, name="update_notification_token"),
]
