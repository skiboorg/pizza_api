from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(Guest)
admin.site.register(UserAddress)
admin.site.register(Promo)

