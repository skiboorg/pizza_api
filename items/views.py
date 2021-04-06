import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from user.models import Guest


class SetDiscount(APIView):
    def get(self,request):
        return Response(status=200)
class RemoveDiscount(APIView):
    def get(self,request):
        return Response(status=200)
class GetBanners(generics.ListAPIView):
    serializer_class = BannerSerializer

    def get_queryset(self):
        return Banners.objects.filter(is_active=True)


class GetItemsByID(generics.RetrieveAPIView):
    serializer_class = FullItemSerializer
    queryset = Item.objects.filter()


class GetCategories(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class GetCities(generics.ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()

class GetItemsByCity(generics.ListAPIView):
    serializer_class = ShortItemSerializer
    def get_queryset(self):
        return Item.objects.filter(city=self.request.query_params.get('city_id'))

class GetSousesByCity(generics.ListAPIView):
    serializer_class = SouceSerializer
    def get_queryset(self):
        return Souce.objects.filter(city=self.request.query_params.get('city_id'))

