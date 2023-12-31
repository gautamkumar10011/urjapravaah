"""
URL configuration for electricManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework.authtoken import views
from django.urls import re_path as url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token, name='api-tokn-auth'),
    url(r'^auth/',include('djoser.urls')),
    path("api/",include('accounts.urls')),
    path('users/', include('accounts.user_urls')),
    path('user/roles/', include('emapp.role.urls')),
    path('api/', include('emapp.dashboard.urls')),
    path('permission/', include('emapp.permission.urls')),
    path('feeder/', include('emapp.feeder.urls')),
    path('feeder/station/mappings/', include('emapp.feederStationMapping.urls')),
    path('schedules/', include('emapp.schedule.urls')),
    path('stations/', include('emapp.station.urls')),
    path('groups/', include('emapp.group.urls')),
]
urlpatterns  +=  static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)