from django.contrib import admin
from emapp.permission.models import UserFeeder
from emapp.permission.models import GroupFeeder

class UserFeederAdmin(admin.ModelAdmin):
    list_display = ('userId','feederId',)
    list_filter = ('userId','feederId',)

class GroupFeederAdmin(admin.ModelAdmin):
    list_display = ('groupId','feederId',)
    list_filter = ('groupId','feederId',)


admin.site.register(UserFeeder,UserFeederAdmin)
admin.site.register(GroupFeeder,GroupFeederAdmin)
