from django.contrib import admin
from .models import *

class AdditionalIngridientPriceInline (admin.TabularInline):
    model = AdditionalIngridientPrice
    extra = 0

class ItemPriceInline (admin.TabularInline):
    model = ItemPrice
    extra = 0

class SoucePriceInline (admin.TabularInline):
    model = SoucePrice
    extra = 0
class CityAdmin(admin.ModelAdmin):
    inlines = [AdditionalIngridientPriceInline,ItemPriceInline,SoucePriceInline]
    class Meta:
        model = City

admin.site.register(City,CityAdmin)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(ItemPrice)
admin.site.register(BaseIngridient)
admin.site.register(AdditionalIngridient)
admin.site.register(AdditionalIngridientPrice)

admin.site.register(Souce)
admin.site.register(SoucePrice)
