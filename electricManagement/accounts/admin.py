from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from accounts import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id','username']
    list_display = ['username','roleId',]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': ('first_name','last_name','email','phone')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'is_public',
                    'play_device',
                    'groups',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
        (_('User Region'), {'fields': ("roleId",'notification_tokens')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2','phone')
            }),
        )



admin.site.register(models.User, UserAdmin)



