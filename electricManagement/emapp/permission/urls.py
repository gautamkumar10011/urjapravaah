from django.urls import path
from django.urls import include, re_path as url
from emapp.permission import views
from emapp.permission import groupViews

urlpatterns = [
	url(r'^create$',views.create_permissions, name='create_permissions'),
	url(r'^delete$',views.delete_permissions, name='delete_permissions'),
	url(r'^feeder/mapping$',views.feeder_mapping, name='feeder_mapping'),
	url(r'^fetch/user$',views.fetch_user, name='fetch_user'),

	url(r'^create/group$',groupViews.create_permissions, name='create_permissions'),
	url(r'^delete/group$',groupViews.delete_permissions, name='delete_permissions'),
	url(r'^group/mapping$',groupViews.group_feeder_mapping, name='group_feeder_mapping'),
	url(r'^fetch/group$',groupViews.fetch_group, name='fetch_group'),
	url(r'^fetch/group/feeder$',groupViews.group_feeder_mapping_only, name='group_feeder_mapping_only'),
	
]
