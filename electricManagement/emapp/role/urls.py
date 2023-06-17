from django.urls import path
from django.urls import include, re_path as url
from emapp.role import views

urlpatterns = [
	url(r'^v1/id$', views.get_role, name='get_role'),
	url(r'^v1/$', views.get_roles, name='get_roles'),
	url(r'^v1/create/$', views.create_role, name='create_role'),
	url(r'^v1/update/$', views.update_role, name='update_role'),
	url(r'^v1/delete/$', views.delete_role, name='delete_role'),
	url(r'^crud/name/and/value$', views.crud_name_n_value, name='crud_name_n_value'),
	url(r'^compnent/names$', views.compnent_name, name='compnent_name'),
]
