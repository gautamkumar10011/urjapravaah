from django.urls import path
from django.urls import include, re_path as url
from emapp.permission import views


urlpatterns = [
	url(r'^create$',views.create_permissions, name='create_permissions'),
	url(r'^delete$',views.delete_permissions, name='delete_permissions'),
	url(r'^feeder/mapping$',views.feeder_mapping, name='feeder_mapping'),
	url(r'^fetch/user$',views.fetch_user, name='fetch_user'),
]
