from django.contrib import admin
from emapp.permission.models import UserFeeder

class UserFeederAdmin(admin.ModelAdmin):
    list_display = ('userId','feederId',)
    list_filter = ('userId','feederId',)

admin.site.register(UserFeeder,UserFeederAdmin)
