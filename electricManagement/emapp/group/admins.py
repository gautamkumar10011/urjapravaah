from django.contrib import admin
from emapp.group.models import GroupModel
# Register your models here.

class GroupAdmin(admin.ModelAdmin):
    list_display = ('seq_num' ,'name' ,)
    search_fields = ('seq_num' ,'name' ,)

admin.site.register(GroupModel,GroupAdmin)