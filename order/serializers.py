from rest_framework import serializers
from .models import *
from items.models import City
from courier.models import Courier


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'id',
            'name'
        ]
class CourierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Courier
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    courier = CourierSerializer(many=False,required=False,read_only=True)
    city = CitySerializer(many=False,required=False,read_only=True)
    class Meta:
        model = Order
        fields = '__all__'







