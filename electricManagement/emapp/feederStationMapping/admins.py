from django.contrib import admin
from emapp.feederStationMapping.models import FeederStationModel
# Register your models here.

class FeederStationAdmin(admin.ModelAdmin):
    list_display = ('stationId' ,'feederId' ,)


admin.site.register(FeederStationModel, FeederStationAdmin)