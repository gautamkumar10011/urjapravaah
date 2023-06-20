from django.contrib import admin
from emapp.permission.models import UserFeeder

class UserFeederAdmin(admin.ModelAdmin):
    list_display = ('user','feeder',)
    list_filter = ('user','feeder',)

admin.site.register(UserFeeder,UserFeederAdmin)
