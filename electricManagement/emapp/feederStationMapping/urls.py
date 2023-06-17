from django.urls import path
from django.urls import include, re_path as url
from emapp.feederStationMapping import views

urlpatterns = [
	url(r'^v1/id$', views.get_feederStation, name='get_feederStation'),
	url(r'^v1/$', views.get_feederStations, name='get_feederStations'),
	url(r'^v1/create/$', views.create_feederStation, name='create_feederStation'),
	url(r'^v1/update/$', views.update_feederStation, name='update_feederStation'),
	url(r'^v1/delete/$', views.delete_feederStation, name='delete_feederStation'),
]