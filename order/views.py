import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from cart.services import *
from user.models import Guest
from random import choices
import string
import requests
from django.views.decorators.clickjacking import xframe_options_exempt
from django.shortcuts import render,HttpResponseRedirect
from .services import *
from promotion.models import *

import settings

from django.utils import timezone
from items.models import City
from yookassa import Configuration, Payment as YooPayment

import logging

logger = logging.getLogger(__name__)

@xframe_options_exempt
def pay_fail(request):
        return HttpResponseRedirect(f'{settings.RETURN_URL}/order/fail')


class YooPaySuccess(APIView):
    def post(self,request):
        status = request.data['object']['status']
        source = request.GET.get('source')
        logger.info(request.data)
        if status == 'succeeded':

            payment = Payment.objects.get(sberId=request.data['object']['id'])
            if not payment.order.is_payed:
                payment.status = True
                payment.save()
                payment.order.is_payed = True
                payment.order.save()
                generate_pdf(payment.order, payment.order.cart)
            if source == 'mobile':
                return render(request, 'pay_success.html', locals())
            else:
                return HttpResponseRedirect(f'{settings.RETURN_URL}/order/{payment.order.order_code}')


@xframe_options_exempt
def pay_success(request):
    payment_id = request.GET.get('orderId')
    source = request.GET.get('source')
    print(source)
    payment = Payment.objects.get(sberId=payment_id)
    if not payment.order.is_payed:

        payment.status = True
        payment.save()
        payment.order.is_payed = True
        payment.order.save()
        generate_pdf(payment.order,payment.order.cart)
    if source=='mobile':
        return render(request, 'pay_success.html', locals())
    else:
        return HttpResponseRedirect(f'{settings.RETURN_URL}/order/{payment.order.order_code}')


class NewOrder(APIView):
    def post(self,request):
        data = request.data
        session_id = data.get('session_id')
        cart = check_if_cart_exists(request, session_id)
        print_log(f'order start | cart {cart}')
        print_log(f'data {data.get("data")}')
        print_log(f'source {data.get("source")}')
        print_log(f'cart {cart.items.all()}')

        print(data.get('data'))
        city_id = data.get('city_id')
        source = data.get('source')
        order_data = data.get('data')
        cafe_address = order_data.get('cafe_address')
        email = cafe_address['order_email']
        print(email)




        try:
            curr_promo = Promotion.objects.get(is_first_order=True)
            promo_is_use = PromotionUse.objects.get(promotion=curr_promo, user=cart.client, is_saved=False)
            promo_is_use.is_saved = True
            promo_is_use.save()
        except:
            pass

        city = City.objects.get(id=city_id)

        new_order = Order.objects.create(
            cart=cart,
            city_id=city_id,
            name=order_data.get('name'),
            phone=order_data.get('phone'),
            phone_raw=order_data.get('phone_raw'),
            payment=order_data.get('payment'),
            delivery_type=order_data.get('delivery_type'),
            need_callback=order_data.get('need_callback'),
            no_cashback=order_data.get('no_cashback'),
            persons = cart.persons,
            comment=order_data.get('comment'),
            date = order_data.get('date').replace('/','-'),
            time=order_data.get('time'),
            price=cart.total_price - data.get('bonuses'),
            bonuses=data.get('bonuses'),
            cafe_address=cafe_address['address'],
            promo=data.get('promo'),
            cashback=order_data.get('cashback') if order_data.get('cashback') else 0,
            street=order_data.get('street'),
            house=order_data.get('house'),
            flat=order_data.get('flat'),
            podezd=order_data.get('podezd'),
            code=order_data.get('code'),
            floor=order_data.get('floor'),
            source=source,
            email=email,
            is_new=True
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

        # all_cart_items = cart.items.all()
        # all_cart_constructors = cart.pizza_constructors.all()
        # all_cart_souses = cart.souces.all()
        #
        # for i in all_cart_items:
        #     new_order.order_content += f'{i.item.name} X {i.quantity} ('
        #     for b_i in i.base_ingridients.all():
        #         if not b_i.is_removed:
        #             new_order.order_content += f'{b_i.item.name} '
        #     for a_i in i.additional_ingridients.all():
        #         if a_i.is_added:
        #             new_order.order_content += f'{a_i.item.name} '
        #     new_order.order_content += f')\n '
        # for i in all_cart_constructors:
        #     text = ''
        #     for i_p in i.items.all():
        #         text += f'{i_p.name} '
        #     new_order.order_content += f'Конструктор {text} X {i.quantity} \n'
        # for i in all_cart_souses:
        #     new_order.order_content += f'{i.item.name} X {i.quantity} '

        new_order.order_code = f''.join(choices(string.digits, k=2))+'-'+ f''.join(choices(string.digits, k=6))
        if data.get('promo') > 0:
            new_order.price = new_order.price - (new_order.price * data.get('promo') / 100)
        if new_order.delivery_type == 'Курьером':
            new_order.price += city.delivery_price
        new_order.save()

        if new_order.payment == 'online':
            new_order.is_payed = False
            new_order.save()
            Configuration.account_id = new_order.city.shopID
            Configuration.secret_key = new_order.city.secretKey
            Configuration.configure(new_order.city.shopID, new_order.city.secretKey)
            print(new_order.city.shopID)
            print(new_order.city.secretKey)
            pay_id = uuid.uuid4()

            print_log(f'order go payment | order_code {new_order.order_code}')

            payment = YooPayment.create({
                "amount": {
                    "value": new_order.price,
                    "currency": "RUB"
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": f"https://meat-coal.ru"
                },
                "capture": True,
                "description": f"Оплата заказа {new_order.order_code}"
            }, uuid.uuid4())

            response = json.loads(payment.json())
            print(response)

            # print('username',new_order.city.sber_login)
            # print('pass',new_order.city.sber_pass)
            # response = requests.get(f'{new_order.city.sber_url}?'
            #                         f'amount={new_order.price}00&'
            #                         'currency=643&'
            #                         'language=ru&'
            #                         f'orderNumber={new_order.order_code}&'
            #                         f'description=Оплата заказа {new_order.order_code}.&'
            #                         f'password={new_order.city.sber_pass}&'
            #                         f'userName={new_order.city.sber_login}&'
            #                         f'returnUrl={settings.SBER_API_RETURN_URL+source}&'
            #                         f'failUrl={settings.SBER_API_FAIL_URL+source}&'
            #                         'pageView=DESKTOP&sessionTimeoutSecs=1200',
            #                         verify='Cert_CA.pem')
            # response_data = json.loads(response.content)
            #
            # print(response_data)

            formUrl = response['confirmation']['confirmation_url']
            payment_id = response.get('id')

            # formUrl = response_data.get('formUrl')
            # payment_id = response_data.get('orderId')

            if formUrl:
                Payment.objects.create(sberId=payment_id,
                                       order=new_order,
                                       amount=new_order.price)
                return Response({
                    'formUrl': formUrl,
                    'p_id': payment_id
                    },
                    status=200)
        else:
            print_log(f'order go generate email | order_code {new_order.order_code}')
            print_log(f'cart {cart.items.all()}')
            generate_pdf(new_order,cart)
            return Response({'code': new_order.order_code}, status=200)


class GetUserOrders(generics.ListAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        return Order.objects.filter(client=self.request.user).order_by('-created_at')

class GetOrders(generics.ListAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        # yesterday = datetime.date.today() - datetime.timedelta(days=1)
        # print(yesterday)
        dt = timezone.now()
        start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        # print(Order.objects.filter(city_id=self.request.query_params.get('city_id'),
        #                             delivery_type='Курьером',
        #                             date=start).order_by('-created_at'))
        return Order.objects.filter(city_id=self.request.query_params.get('city_id'),
                                    # delivery_type='Курьером',
                                    date=start).order_by('-created_at')



class SetOrderView(APIView):
    def get(self, request):
        order = Order.objects.get(id=self.request.query_params.get('id'))
        order.is_new = False
        order.save()
        return Response(status=200)
class Stats(APIView):
    def get(self,request):
        orders = Order.objects.all()
        phones = []
        total_summ = 0
        for order in orders:
            total_summ += order.price
            phones.append(order.phone)
        total_phones = len(list(dict.fromkeys(phones)))
        pp = ''
        for p in list(dict.fromkeys(phones)):
            pp += f'{p},'

        return Response({
            'Всего заказов':orders.count(),
            'Общая сумма заказов':total_summ,
            'Средний чек':total_summ / orders.count(),
            'Уникальных номеров':total_phones,
            'Телефоны':pp,

        },status=200)
