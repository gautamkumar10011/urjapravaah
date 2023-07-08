from django.urls import path
from django.urls import include, re_path as url
from emapp.group import views

urlpatterns = [
	url(r'^v1/id$', views.get_group, name='get_group'),
	url(r'^v1/$', views.get_groups, name='get_groups'),
	url(r'^v1/create/$', views.create_group, name='create_group'),
	url(r'^v1/update/$', views.update_group, name='update_group'),
	url(r'^v1/delete/$', views.delete_group, name='delete_group'),
]