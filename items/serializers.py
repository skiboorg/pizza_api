from rest_framework import serializers
from .models import *

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CafeAddress
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    adresses = AddressSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = City
        fields = '__all__'


class ItemPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPrice
        fields = [
            'city',
            'old_price',
            'price',
            'price_33',
        ]


class CategoryItemSerializer(serializers.ModelSerializer):
    base_ingridients = serializers.SerializerMethodField()
    is_pizza = serializers.SerializerMethodField()
    is_meat = serializers.SerializerMethodField()
    kbgu = serializers.SerializerMethodField()
    prices = ItemPriceSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Item
        # fields = '__all__'
        exclude = [
            'city',
            'additional_ingridients',
            'order_num',
            'code',
            'discount',
            'is_recommended',
            'is_new',
            'buys',
            'created_at',
            'category',
            'weight_33',
            'callories',
            'fat',
            'belki',
            'uglevod',
        ]

    def get_base_ingridients(self,obj):
        val = ''
        items = obj.base_ingridients.all()
        for item in items:
            val += f'{item.name.lower()}, '
        return val[:-2]

    def get_is_pizza(self, obj):
        return obj.category.is_pizza


    def get_is_meat(self, obj):
        return obj.category.is_meat



    def get_kbgu(self, obj):
        if obj.callories > 0:
            return f'{obj.callories}/{obj.fat}/{obj.belki}/{obj.uglevod}'
        else:
            return ''

class CategorySerializer(serializers.ModelSerializer):
    items = CategoryItemSerializer(many=True,required=False,read_only=True)
    class Meta:
        model = Category
        fields = '__all__'




class BaseIngridientSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseIngridient
        fields = '__all__'


# class AdditionalIngridientSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = AdditionalIngridient
#         fields = '__all__'


class AdditionalIngridientPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalIngridientPrice
        fields = [
            'city',
            'price',
        ]


class AdditionalIngridientSerializer(serializers.ModelSerializer):
    price = AdditionalIngridientPriceSerializer(many=True)
    class Meta:
        model = AdditionalIngridient
        fields = '__all__'

class ShortCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SimpleItemSerializer(serializers.ModelSerializer):
    prices = ItemPriceSerializer(many=True, required=False, read_only=True)
    category = ShortCategorySerializer(many=False, required=False, read_only=True)

    class Meta:
        model = Item
        fields = '__all__'


class RecommendedItemSerializer(serializers.ModelSerializer):
    prices = ItemPriceSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Item
        exclude = [
            'category',
            'additional_ingridients',
            'base_ingridients',
            'discount',
            'created_at',
            'is_new',
            'buys',
            'code',
            'weight_33',
            'city',
            'callories',
            'fat',
            'belki',
            'uglevod',
            'unit_name',
            'min_unit',
            'weight',
            'is_recommended',
            'is_for_meat',
            'is_gift',
            'is_active',
            'order_num',
        ]


class ShortItemSerializer(serializers.ModelSerializer):
    category = ShortCategorySerializer(many=False, required=False, read_only=True)
    base_ingridients = serializers.SerializerMethodField()
    prices = ItemPriceSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Item
        exclude = ['additional_ingridients','discount','created_at','is_new','buys','code','weight_33','city']

    def get_base_ingridients(self,obj):
        val = ''
        items = obj.base_ingridients.all()
        for item in items:
            val += f'{item.name.lower()}, '
        return val[:-2]


# CategorySerializer > ShortCategorySerializer
class FullItemSerializer(serializers.ModelSerializer):
    category = ShortCategorySerializer(many=False, required=False, read_only=True)
    base_ingridients = BaseIngridientSerializer(many=True, required=False, read_only=True)
    additional_ingridients = AdditionalIngridientSerializer(many=True, required=False, read_only=True)
    prices = ItemPriceSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Item
        fields = '__all__'

class SoucePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoucePrice
        fields = [
            'city',
            'price',
        ]


class SouceSerializer(serializers.ModelSerializer):
    prices = SoucePriceSerializer(many=True)
    class Meta:
        model = Souce
        fields = '__all__'



# class ItemTypeSerializer(serializers.ModelSerializer):
#     item = ItemSerializer(many=False, read_only=True, required=False)
#     color = ItemColorSerializer(many=False, read_only=True, required=False)
#     size = ItemSizeSerializer(many=False, read_only=True, required=False)
#     height = ItemHeightSerializer(many=False, read_only=True, required=False)
#
#     class Meta:
#         model = ItemType
#         fields = '__all__'

