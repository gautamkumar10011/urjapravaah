from django.urls import path
from django.urls import include, re_path as url
from emapp.station import views

urlpatterns = [
	url(r'^v1/id$', views.get_station, name='get_station'),
	url(r'^v1/$', views.get_stations, name='get_stations'),
	url(r'^v1/create/$', views.create_station, name='create_station'),
	url(r'^v1/update/$', views.update_station, name='update_station'),
	url(r'^v1/delete/$', views.delete_station, name='delete_station'),
	url(r'^v1/fetch/feeder/by/station/id/$', views.get_feeder_by_station_id, name='get_feeder_by_station_id'),
]