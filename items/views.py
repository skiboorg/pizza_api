import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from user.models import Guest
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class SetPizzaDiscount(APIView):
    def get(self,request):
        items = Item.objects.filter(category_id=1)
        x=0
        for item in items:
            if not item.is_gift:
                item_price = ItemPrice.objects.get(city_id=1,item=item)
                if item_price.old_price == 0:

                    item_price.old_price = item_price.price
                    item_price.old_price_33 = item_price.price_33

                    item_price.price = int(item_price.price - item_price.price * 30 /100)
                    item_price.price_33 = int(item_price.price_33 - item_price.price_33 * 30 /100)
                    item_price.save()
                    x+=1
        return Response({'Изменено товаров':x}, status=200)


class RemovePizzaDiscount(APIView):
    def get(self, request):
        items = Item.objects.filter(category_id=1)
        x = 0
        for item in items:
            if not item.is_gift:
                item_price = ItemPrice.objects.get(city_id=1, item=item)
                if item_price.old_price > 0:
                    item_price.price = item_price.old_price
                    item_price.price_33 = item_price.old_price_33
                    item_price.old_price = 0
                    item_price.old_price_33 = 0
                    item_price.save()
                    x += 1
        return Response({'Изменено товаров': x}, status=200)



class SetDiscount(APIView):
    def get(self,request):
        items = Item.objects.filter(category_id=4)
        x=0
        for item in items:
            if not item.is_gift:
                item_price = ItemPrice.objects.get(city_id=1,item=item)
                if item_price.old_price == 0:
                    item_price.old_price = item_price.price
                    item_price.price = int(item_price.price - item_price.price * 35 /100)
                    item_price.save()
                    x+=1
        return Response({'Изменено товаров':x}, status=200)


class RemoveDiscount(APIView):
    def get(self,request):
        items = Item.objects.filter(category_id=4)
        x = 0
        for item in items:
            if not item.is_gift:
                item_price = ItemPrice.objects.get(city_id=1, item=item)
                if item_price.old_price>0:
                    item_price.price = item_price.old_price
                    item_price.old_price = 0
                    item_price.save()
                    x += 1
        return Response({'Изменено товаров': x}, status=200)


class GetBanners(generics.ListAPIView):
    serializer_class = BannerSerializer

    def get_queryset(self):
        return Banners.objects.filter(is_active=True, city=self.request.query_params.get('city_id'))

    # @method_decorator(cache_page(60 * 60 * 2))
    def dispatch(self, *args, **kwargs):
        return super(GetBanners, self).dispatch(*args, **kwargs)


class GetRecommendedItems(generics.ListAPIView):
    serializer_class = RecommendedItemSerializer
    def get_queryset(self):
        return Item.objects.filter(city=self.request.query_params.get('city_id'), is_recommended=True, is_active=True)

    # @method_decorator(cache_page(60 * 60 * 2))
    def dispatch(self, *args, **kwargs):
        return super(GetRecommendedItems, self).dispatch(*args, **kwargs)


class GetRecommendedItemsForMeat(generics.ListAPIView):
    serializer_class = RecommendedItemSerializer

    def get_queryset(self):
        return Item.objects.filter(city=self.request.query_params.get('city_id'), is_for_meat=True, is_active=True)

    # @method_decorator(cache_page(60 * 60 * 2))
    def dispatch(self, *args, **kwargs):
        return super(GetRecommendedItemsForMeat, self).dispatch(*args, **kwargs)

class GetItemsByID(generics.RetrieveAPIView):
    serializer_class = FullItemSerializer
    queryset = Item.objects.filter()



class GetCategories(generics.ListAPIView):

    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(city=self.request.query_params.get('city_id'))

    #@method_decorator(cache_page(60 * 60 * 2))
    # def dispatch(self, *args, **kwargs):
    #     return super(GetCategories, self).dispatch(*args, **kwargs)





class GetCities(generics.ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()

class GetCity(generics.RetrieveAPIView):
    serializer_class = CitySerializer
    def get_object(self):
        return City.objects.get(domain=self.request.query_params.get('domain'))

class GetItemsByCity(generics.ListAPIView):
    serializer_class = ShortItemSerializer
    def get_queryset(self):
        return Item.objects.filter(is_active=True, city=self.request.query_params.get('city_id'))

    #@method_decorator(cache_page(60 * 60 * 2))
    def dispatch(self, *args, **kwargs):
        return super(GetItemsByCity, self).dispatch(*args, **kwargs)

class GetSousesByCity(generics.ListAPIView):
    serializer_class = SouceSerializer
    def get_queryset(self):
        return Souce.objects.filter(city=self.request.query_params.get('city_id'))

    # @method_decorator(cache_page(60 * 60 * 2))
    def dispatch(self, *args, **kwargs):
        return super(GetSousesByCity, self).dispatch(*args, **kwargs)

class CopyCity(APIView):
    def get(self,request):
        target_id = self.request.query_params.get('target_id')
        new_name = self.request.query_params.get('new_name')
        domain_name = self.request.query_params.get('domain_name')

        city = City.objects.get(id=target_id)
        new_city = City.objects.create(
            name=new_name,
            modalText=city.modalText,
            info=city.info,
            order_email=city.order_email,
            order_phone=city.order_phone,
            domain=domain_name,
            sber_login=city.sber_login,
            sber_pass=city.sber_pass,
            sber_url=city.sber_url,
            main_phone=city.main_phone,
            contacts_text=city.contacts_text,
            payment_text=city.payment_text,
            delivery_times=city.delivery_times,
            delivery_from_price=city.delivery_from_price,
            delivery_price=city.delivery_price,
            delivery_time=city.delivery_time,
            about_image=city.about_image,
            about_kitchen=city.about_kitchen,
            vk_link=city.vk_link,
            inst_link=city.inst_link,
            policy_text=city.policy_text,
            rules_text=city.rules_text,
        )

        categories = Category.objects.all()

        for cat in categories:
            cat.city.add(new_city)



        itemprices = ItemPrice.objects.filter(city_id__in=[city.id])

        for itemprice in itemprices:
            print(itemprice)
            itemprice.item.city.add(new_city)
            ItemPrice.objects.create(
                city=new_city,
                item=itemprice.item,
                old_price=itemprice.old_price,
                old_price_33=itemprice.old_price_33,
                price=itemprice.price,
                price_33=itemprice.price_33,
            )

        souceprices = SoucePrice.objects.filter(city=city)
        print('-----------------')
        for souceprice in souceprices:
            print(souceprice)
            SoucePrice.objects.create(
                city=new_city,
                item=souceprice.item,
                price=souceprice.price,
            )
        addprices = AdditionalIngridientPrice.objects.filter(city=city)

        print('-----------------')
        for addprice in addprices:
            print(addprice)
            AdditionalIngridientPrice.objects.create(
                city=new_city,
                ingridient=addprice.ingridient,
                price=addprice.price,
            )
