from django.contrib import admin
from .models import *


class OrdersInline (admin.TabularInline):
    model = CourierOrder
    extra = 0

class CourierAdmin(admin.ModelAdmin):
    inlines = [OrdersInline]
    class Meta:
        model = Courier

admin.site.register(Courier,CourierAdmin)