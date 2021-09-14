import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from order.models import Order
from user.services import sendPush

class GetCourier(generics.RetrieveAPIView):
    serializer_class = CourierSerializer
    def get_object(self):
        courier = None
        phone=self.request.query_params.get('phone').replace('+','').replace(' ','').replace('(','').replace(')','').replace('-','')
        print(phone)
        try:
            courier = Courier.objects.get(phone=phone)
        except:
            pass
        return courier

class GetAllCouriers(generics.ListAPIView):
    serializer_class = CourierSerializer
    def get_queryset(self):
        print(self.request.query_params.get('city_id'))
        print(Courier.objects.filter(city_id=self.request.query_params.get('city_id')))
        return Courier.objects.filter(city_id=self.request.query_params.get('city_id'))

class SetToken(APIView):
    def post(self, request):
        print(request.data)
        courier = Courier.objects.get(id=request.data.get('courier_id'))
        courier.notification_id = request.data.get('notification_id')
        courier.save()
        return Response(status=200)

class DeliveryComplete(APIView):
    def post(self, request):
        print(request.data)
        order = Order.objects.get(id=request.data.get('order_id'))
        courier = Courier.objects.get(id=request.data.get('courier_id'))
        courier.have_orders_in_delivery = False
        order.is_delivered = True
        order.is_delivery_in_progress = False
        order.is_assing = False
        order.is_payed = True
        order.save()
        courier.save()
        return Response(status=200)

class GetCoordinates(APIView):
    def get(self, request):
        print(request.GET)
        order =  Order.objects.get(id=request.GET['id'])
        print(order)
        return Response({'coords':order.courier.coordinates}, status=200)

class UpdateCoordinates(APIView):
    def post(self, request):
        print(request.data)
        courier = Courier.objects.get(id=request.data.get('courier_id'))
        courier.coordinates = request.data.get('coordinates')
        courier.save()
        return Response(status=200)

class OrderInDelivery(APIView):
    def post(self, request):
        print(request.data)
        order = Order.objects.get(id=request.data.get('order_id'))
        courier = Courier.objects.get(id=request.data.get('courier_id'))
        order.is_delivery_in_progress = True
        order.save()
        courier.have_orders_in_delivery = True
        courier.save()
        if order.client and order.client.notification_id:
            sendPush('client', 'single','Обновление статуса заказа',
                     f'Курьер начал доставку заказа №{order.order_code}',n_id=order.client.notification_id)
        return Response(status=200)

class AssingOrder(APIView):
    def post(self,request):
        print(request.data)
        order = Order.objects.get(id=request.data.get('order_id'))
        courier = Courier.objects.get(id=request.data.get('courier_id'))
        CourierOrder.objects.create(courier=courier,order=order)
        if order.client and order.client.notification_id:
            sendPush('client', 'single','Обновление статуса заказа',f'Заказ №{order.order_code} назначен курьеру',n_id=order.client.notification_id)
        if courier.notification_id:
            sendPush('courier', 'single', 'Назначен заказ', f'Вам назначен заказ №{order.order_code}',
                     n_id=courier.notification_id)
        return Response(status=200)