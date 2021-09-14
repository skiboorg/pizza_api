from rest_framework import serializers
from .models import *
from items.serializers import *
from order.models import Order
from items.models import City



class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'id',
            'name'
        ]

class OrderSerializer(serializers.ModelSerializer):
    city = CitySerializer(many=False, required=False, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class CourierOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer(many=False, read_only=True, required=False)
    class Meta:
        model = CourierOrder
        fields = '__all__'

class CourierSerializer(serializers.ModelSerializer):
    orders = CourierOrderSerializer(many=True, read_only=True, required=False)
    class Meta:
        model = Courier
        fields = '__all__'


