from django.contrib import admin
from emapp.schedule.models import ScheduleModel
# Register your models here.

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('status' ,)
    search_fields = ('status' ,)


admin.site.register(ScheduleModel,ScheduleAdmin)