from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class UserAdmin(BaseUserAdmin):
    list_display = ('phone',)
    ordering = ('id',)
    search_fields = ('phone',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone',  'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info',
         {'fields': (
             'phone',
             'city',
             'promo',
             'fio',
             'bonuses',

         )}
         ),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',)}),)

admin.site.register(User,UserAdmin)
admin.site.register(Guest)
admin.site.register(UserAddress)
admin.site.register(Promo)

