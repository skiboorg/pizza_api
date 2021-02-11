from rest_framework import serializers
from .models import *
from items.serializers import *

class CartItemSerializer(serializers.ModelSerializer):
    item = SimpleItemSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = CartItem
        fields = '__all__'


class PizzaConstructorSerializer(serializers.ModelSerializer):
    items = SimpleItemSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = CartConstructor
        fields = '__all__'

class CartSouceSerializer(serializers.ModelSerializer):
    item = SouceSerializer(many=False, required=False, read_only=True)
    class Meta:
        model = CartSouce
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    pizza_constructors = PizzaConstructorSerializer(many=True, read_only=True, required=False)
    souces = CartSouceSerializer(many=True, read_only=True, required=False)
    items = CartItemSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Cart
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

