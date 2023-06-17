from django.contrib import admin
from emapp.feeder.models import FeederModel
# Register your models here.

class FeederAdmin(admin.ModelAdmin):
    list_display = ('seq_num' ,'name' ,)
    search_fields = ('seq_num' ,'name' ,)

admin.site.register(FeederModel,FeederAdmin)