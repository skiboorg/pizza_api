import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
#from .serializers import *
from .models import *
from cart.services import *
from user.models import Guest
from random import choices
import string
import settings
import requests


class NewOrder(APIView):
    def post(self,request):
        data = request.data
        session_id = data.get('session_id')
        order_data = data.get('data')
        print(data)
        cart = check_if_cart_exists(request, session_id)
        new_order = Order.objects.create(
            name=order_data.get('name'),
            phone=order_data.get('phone'),
            payment=order_data.get('payment'),
            delivery_type=order_data.get('delivery_type'),
            need_callback=order_data.get('need_callback'),
            no_cashback=order_data.get('no_cashback'),
            # persons = 1,order_data.get('persons'),
            # comment =order_data.get('comment'),
            # date = order_data.get('date'),
            time = order_data.get('time'),
            price = cart.total_price - data.get('bonuses') - data.get('promo'),
            bonuses =data.get('bonuses'),
            promo = data.get('promo'),
            cashback = order_data.get('cashback'),
            street = order_data.get('street'),
            house = order_data.get('house'),
            flat = order_data.get('flat'),
            podezd = order_data.get('podezd'),
            code = order_data.get('code'),
            floor =order_data.get('floor')
        )
        user = cart.client
        guest = cart.guest

        if user:
            new_order.client = user
            user.bonuses -= data.get('bonuses')
            user.bonuses += cart.total_bonuses
            user.save()
        if guest:
            new_order.guest = guest

        all_cart_items = cart.items.all()
        all_cart_constructors = cart.pizza_constructors.all()
        all_cart_souses = cart.souces.all()

        for i in all_cart_items:
            new_order.order_content += f'{i.item.name} X {i.quantity} ('
            for b_i in i.base_ingridients.all():
                if not b_i.is_removed:
                    new_order.order_content += f'{b_i.item.name} '
            for a_i in i.additional_ingridients.all():
                if a_i.is_added:
                    new_order.order_content += f'{a_i.item.name} '
            new_order.order_content += f')\n '
        for i in all_cart_constructors:
            text=''
            for i_p in i.items.all():
                text += f'{i_p.name} '
            new_order.order_content += f'Конструктор {text} X {i.quantity} \n'
        for i in all_cart_souses:
            new_order.order_content += f'{i.item.name} X {i.quantity} '
        new_order.order_code = f'{new_order.id}-'.join(choices(string.digits, k=3))
        new_order.save()
        # erase_cart(cart)
        if new_order.payment == 'online':
            response = requests.get('https://3dsec.sberbank.ru/payment/rest/register.do?'
                                    f'amount={new_order.price}00&'
                                    'currency=643&'
                                    'language=ru&'
                                    f'orderNumber={new_order.order_code}&'
                                    f'description=Оплата заказа {new_order.order_code}.&'
                                    f'password={settings.SBER_API_PASSWORD}&'
                                    f'userName={settings.SBER_API_LOGIN}&'
                                    f'returnUrl={settings.SBER_API_RETURN_URL}&'
                                    f'failUrl={settings.SBER_API_FAIL_URL}&'
                                    'pageView=DESKTOP&sessionTimeoutSecs=1200')
            response_data = json.loads(response.content)
            print(response_data)
            formUrl = response_data.get('formUrl')
            if formUrl:
                Payment.objects.create(sberId=response_data.get('orderId'),
                                       order=new_order,
                                       amount=new_order.price)
                return Response({'formUrl': formUrl}, status=200)
        else:
            return Response({'code':new_order.order_code}, status=200)
