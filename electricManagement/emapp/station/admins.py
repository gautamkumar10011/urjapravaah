from django.contrib import admin
from emapp.station.models import StationModel
# Register your models here.

class StationAdmin(admin.ModelAdmin):
    list_display = ('seq_num' ,'name' ,)
    search_fields = ('seq_num' ,'name' ,)

admin.site.register(StationModel,StationAdmin)