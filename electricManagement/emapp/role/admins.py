from django.contrib import admin
from emapp.role.models import UserRoleModel
from emapp.role.models import CRUDModel
from emapp.role.models import ComponetName
# Register your models here.

admin.site.register(UserRoleModel)
admin.site.register(CRUDModel)
admin.site.register(ComponetName)
