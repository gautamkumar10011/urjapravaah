from django.urls import path
from django.urls import include, re_path as url
from emapp.dashboard import views

urlpatterns = [
	url(r'^v1/dashboard$', views.get_dashboard, name='get_dashboard'),
]