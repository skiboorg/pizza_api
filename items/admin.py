from django.contrib import admin
from .models import *

class AdditionalIngridientPriceInline (admin.TabularInline):
    model = AdditionalIngridientPrice
    extra = 0

class ItemPriceInline (admin.TabularInline):
    model = ItemPrice
    extra = 0

class AddressInline (admin.TabularInline):
    model = CafeAddress
    extra = 0

class SoucePriceInline (admin.TabularInline):
    model = SoucePrice
    extra = 0
class CityAdmin(admin.ModelAdmin):
    inlines = [AdditionalIngridientPriceInline,ItemPriceInline,SoucePriceInline,AddressInline]
    class Meta:
        model = City
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['order_num', 'name']
    class Meta:
        model = Category

class ItemAdmin(admin.ModelAdmin):
    list_filter = ('city','category','is_recommended','is_active','is_gift',)
    list_display = ['order_num', 'name','min_unit','unit_name', 'is_recommended','is_active']
    class Meta:
        model = Item

admin.site.register(City,CityAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(ItemPrice)
admin.site.register(BaseIngridient)
admin.site.register(AdditionalIngridient)
admin.site.register(AdditionalIngridientPrice)

admin.site.register(Souce)
admin.site.register(SoucePrice)
admin.site.register(Banners)
