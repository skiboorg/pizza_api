from rest_framework import serializers
from .models import *


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
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



class ItemPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPrice
        fields = [
            'city',
            'price',
        ]

class SimpleItemSerializer(serializers.ModelSerializer):
    prices = ItemPriceSerializer(many=True, required=False, read_only=True)
    category = CategorySerializer(many=False, required=False, read_only=True)
    class Meta:
        model = Item
        fields = '__all__'

class ShortItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, required=False, read_only=True)
    base_ingridients = BaseIngridientSerializer(many=True, required=False, read_only=True)
    prices = ItemPriceSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Item
        fields = '__all__'

class FullItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, required=False, read_only=True)
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

