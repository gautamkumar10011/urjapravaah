from django.urls import path
from django.urls import include, re_path as url
from emapp.schedule import views

urlpatterns = [
	url(r'^v1/id$', views.get_schedule, name='get_schedule'),
	url(r'^v1/$', views.get_schedules, name='get_schedules'),
	url(r'^v1/create/$', views.create_schedule, name='create_schedule'),
	url(r'^v1/update/$', views.update_schedule, name='update_schedule'),
	url(r'^v1/delete/$', views.delete_schedule, name='delete_schedule'),
]