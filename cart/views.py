import json

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from .services import *
from user.models import Guest
import settings


class AddPerson(APIView):

    def post(self, request):
        data = request.data
        session_id = data.get('session_id')
        cart = check_if_cart_exists(request, session_id)
        cart.persons += 1
        cart.save()
        return Response(status=200)


class DelPerson(APIView):

    def post(self, request):
        data = request.data
        session_id = data.get('session_id')
        cart = check_if_cart_exists(request, session_id)
        if cart.persons > 1:
            cart.persons -= 1
            cart.save()
        return Response(status=200)


class DeleteItem(APIView):
    def post(self, request):
        data = request.data
        code = data.get('code')
        cart_item = CartItem.objects.get(code=code)
        cart = Cart.objects.get(items=cart_item)
        remove_cart_item(cart_item)
        calculate_total_cart_price(cart)
        return Response(status=200)


class RemoveItemQuantity(APIView):
    def post(self, request):
        data = request.data
        cart_item = CartItem.objects.get(code=data.get('code'))
        cart = Cart.objects.get(items=cart_item)
        if cart_item.quantity > 1 :
            cart_item.quantity -= 1
            cart_item.price -= cart_item.price_per_unit
            cart_item.bonuses = cart_item.price * settings.BONUS_PERCENT

            cart_item.save()
        else:
            remove_cart_item(cart_item)
        calculate_total_cart_price(cart)
        return Response(status=200)


class AddItemQuantity(APIView):
    def post(self, request):
        data = request.data
        cart_item = CartItem.objects.get(code=data.get('code'))
        cart = Cart.objects.get(items=cart_item)
        cart_item.quantity += 1
        cart_item.price += cart_item.price_per_unit
        cart_item.bonuses = cart_item.price * settings.BONUS_PERCENT
        cart_item.save()
        calculate_total_cart_price(cart)
        return Response(status=200)


class RemoveConstructorQuantity(APIView):
    def post(self, request):
        data = request.data
        cart_constructor = CartConstructor.objects.get(code=data.get('code'))
        cart = Cart.objects.get(pizza_constructors=cart_constructor)
        if cart_constructor.quantity > 1 :
            cart_constructor.quantity -= 1
            cart_constructor.price -= cart_constructor.price_per_unit
            cart_constructor.bonuses = cart_constructor.price * settings.BONUS_PERCENT
            cart_constructor.save()
        else:
            cart_constructor.delete()
        calculate_total_cart_price(cart)
        return Response(status=200)


class AddConstructorQuantity(APIView):
    def post(self, request):
        data = request.data
        cart_constructor = CartConstructor.objects.get(code=data.get('code'))
        cart = Cart.objects.get(pizza_constructors=cart_constructor)
        cart_constructor.quantity += 1
        cart_constructor.price += cart_constructor.price_per_unit
        cart_constructor.bonuses = cart_constructor.price * settings.BONUS_PERCENT
        cart_constructor.save()
        calculate_total_cart_price(cart)
        return Response(status=200)


class DeleteCartConstructor(APIView):
    def post(self, request):
        data = request.data
        cart_constructor = CartConstructor.objects.get(code=data.get('code'))
        cart = Cart.objects.get(pizza_constructors=cart_constructor)
        cart_constructor.delete()
        calculate_total_cart_price(cart)
        return Response(status=200)



class AddToCartConstructor(APIView):
    def post(self, request):
        data = request.data
        print(data)
        session_id = data.get('session_id')
        cart = check_if_cart_exists(request, session_id)
        user = cart.client
        guest = cart.guest

        firstPizza = data.get('firstPizza')
        secondPizza = data.get('secondPizza')
        firstPizza_id = firstPizza.get('id')
        secondPizza_id = secondPizza.get('id')
        city_id = data.get('city_id')
        city = City.objects.get(id=city_id)

        firstPizza_price = ItemPrice.objects.get(city=city, item_id=firstPizza_id)
        secondPizza_price = ItemPrice.objects.get(city=city, item_id=secondPizza_id)
        full_price = int((firstPizza_price.price + secondPizza_price.price) / 2)

        code = f'{session_id}_{city_id+firstPizza_id+secondPizza_id}'
        if user:
            try:
                cart_constuctor = CartConstructor.objects.get(code=code)
                cart_constuctor.quantity += 1
                cart_constuctor.price = cart_constuctor.quantity * cart_constuctor.price_per_unit
                cart_constuctor.save()
            except CartConstructor.DoesNotExist:
                cart_constuctor = CartConstructor.objects.create(
                                                                    code=code,
                                                                    client=user,
                                                                    city=city,
                                                                    price_per_unit=full_price,
                                                                    price=full_price,
                                                                    bonuses=full_price * settings.BONUS_PERCENT
                                                                )

        if guest:
            try:
                cart_constuctor = CartConstructor.objects.get(code=code)
                cart_constuctor.quantity += 1
                cart_constuctor.price = cart_constuctor.quantity * cart_constuctor.price_per_unit
                cart_constuctor.save()
            except CartConstructor.DoesNotExist:
                cart_constuctor = CartConstructor.objects.create(
                                                                    code=code,
                                                                    guest=guest,
                                                                    city=city,
                                                                    price_per_unit=full_price,
                                                                    price=full_price,
                                                                    bonuses=full_price * settings.BONUS_PERCENT
                                                                )
        cart_constuctor.items.set([firstPizza_id,secondPizza_id])
        cart.pizza_constructors.add(cart_constuctor)

        calculate_total_cart_price(cart)
        return Response(status=200)


class AddToCartSouse(APIView):
    def post(self, request):
        data = request.data
        print(data)
        session_id = data.get('session_id')
        cart = check_if_cart_exists(request, session_id)

        user = cart.client
        guest = cart.guest

        souse_id = data.get('item_id')
        city_id = data.get('city_id')

        city = City.objects.get(id=city_id)
        souse_price = SoucePrice.objects.get(city=city, item_id=souse_id)

        code = f'{session_id}_{city_id + souse_id}'
        if user:
            try:
                cart_souse = CartSouce.objects.get(code=code)
                cart_souse.quantity += 1
                cart_souse.price = cart_souse.quantity * cart_souse.price_per_unit
                cart_souse.save()
            except CartSouce.DoesNotExist:
                cart_souse = CartSouce.objects.create(
                                                    code=code,
                                                    client=user,
                                                    city=city,
                                                    item_id=souse_id,
                                                    price_per_unit=souse_price.price,
                                                    price=souse_price.price,
                                                    bonuses=souse_price.price * settings.BONUS_PERCENT
                                                )

        if guest:
            try:
                cart_souse = CartSouce.objects.get(code=code)
                cart_souse.quantity += 1
                cart_souse.price = cart_souse.quantity * cart_souse.price_per_unit
                cart_souse.save()
            except CartSouce.DoesNotExist:
                cart_souse = CartSouce.objects.create(
                                                    code=code,
                                                    guest=guest,
                                                    city=city,
                                                    item_id=souse_id,
                                                    price_per_unit=souse_price.price,
                                                    price=souse_price.price,
                                                    bonuses=souse_price.price * settings.BONUS_PERCENT
                                                )

        cart.souces.add(cart_souse)
        calculate_total_cart_price(cart)
        return Response(status=200)


class DeleteCartSouse(APIView):
    def post(self, request):
        data = request.data
        cart_souse = CartSouce.objects.get(code=data.get('code'))
        cart = Cart.objects.get(souces=cart_souse)
        cart_souse.delete()
        calculate_total_cart_price(cart)
        return Response(status=200)


class RemoveCart(APIView):
    def get(self, request):
        items = Cart.objects.all()
        items.delete()
        items = Guest.objects.all()
        items.delete()
        items = CartConstructor.objects.all()
        items.delete()
        items = CartSouce.objects.all()
        items.delete()
        items = CartItemBaseIngrigient.objects.all()
        items.delete()
        items = CartItemAdditionalIngrigient.objects.all()
        items.delete()
        items = CartItem.objects.all()
        items.delete()
        return Response(status=200)

class RemoveSouseQuantity(APIView):
    def post(self, request):
        data = request.data
        cart_souse = CartSouce.objects.get(code=data.get('code'))
        cart = Cart.objects.get(souces=cart_souse)
        if cart_souse.quantity > 1 :
            cart_souse.quantity -= 1
            cart_souse.price -= cart_souse.price_per_unit
            cart_souse.bonuses = cart_souse.price * settings.BONUS_PERCENT
            cart_souse.save()
        else:
            cart_souse.delete()
        calculate_total_cart_price(cart)
        return Response(status=200)


class AddSouseQuantity(APIView):
    def post(self, request):
        data = request.data
        cart_souse = CartSouce.objects.get(code=data.get('code'))
        cart = Cart.objects.get(souces=cart_souse)
        cart_souse.quantity += 1
        cart_souse.price += cart_souse.price_per_unit
        cart_souse.bonuses = cart_souse.price * settings.BONUS_PERCENT
        cart_souse.save()
        calculate_total_cart_price(cart)
        return Response(status=200)



class AddToCart(APIView):
    def post(self, request):
        data = request.data
        cart = check_if_cart_exists(request, data.get('session_id'))
        add_to_cart(cart, data)
        return Response(status=200)


class DelCartItems(APIView):
    def post(self, request, session_id):
        cart = check_if_cart_exists(request, session_id)
        erase_cart(cart)
        return Response(status=200)


class GetCart(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    def get_object(self):
        cart = check_if_cart_exists(self.request, self.request.query_params.get('session_id'))
        return cart




