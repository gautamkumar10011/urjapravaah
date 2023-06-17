from django.urls import path
from django.urls import include, re_path as url
from . import user_manager
from . import views


urlpatterns = [
	url(r'^by/id$',  user_manager.get_user_by_id, name="get_user_by_id"),
	url(r'^all$',   user_manager.get_all_users, name="get_all_users"),
	url(r'^create$', user_manager.create_user, name="create_user"),
	url(r'^update$', user_manager.update_user, name="update_user"),
	url(r'^delete$', user_manager.delete_user, name="delete_user"),
]
