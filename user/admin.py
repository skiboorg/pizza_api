from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


class UserAdmin(BaseUserAdmin):
    list_display = ('phone',)
    ordering = ('id',)
    search_fields = ('phone',)
admin.site.register(User,UserAdmin)
admin.site.register(Guest)
admin.site.register(UserAddress)
admin.site.register(Promo)

