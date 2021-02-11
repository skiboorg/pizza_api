from django.contrib import admin
from .models import *

admin.site.register(CartItemBaseIngrigient)
admin.site.register(CartItemAdditionalIngrigient)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(CartSouce)
admin.site.register(CartConstructor)
