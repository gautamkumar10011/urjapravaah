from django.urls import path
from django.urls import include, re_path as url
from emapp.feeder import views

urlpatterns = [
	url(r'^v1/id$', views.get_feeder, name='get_feeder'),
	url(r'^v1/$', views.get_feeders, name='get_feeders'),
	url(r'^v1/create/$', views.create_feeder, name='create_feeder'),
	url(r'^v1/update/$', views.update_feeder, name='update_feeder'),
	url(r'^v1/delete/$', views.delete_feeder, name='delete_feeder'),
]