import json
import uuid
import requests
from random import choices
import string
from django.http import HttpResponseRedirect
from .services import create_random_string, send_tg_mgs

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import send_sms
from .serializers import *
from .models import *
from rest_framework import generics

import settings


class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        print(request.data)


        serializer = UserSerializer(user, data=request.data['userData'])
        if serializer.is_valid():
            serializer.save()
            user.tg_id = None
            user.save()
            return Response(status=200)
        else:
            print(serializer.errors)
            return Response(status=400)

class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    print(serializer_class.data)
    def get_object(self):
        return self.request.user
    # def get(self, request):
    #     user = request.user
    #     serializer = UserSerializer(user, many=False)
    #     return Response(serializer.data)


class UserRecoverPassword(APIView):
    def post(self,request):
        user = None
        try:
            user = User.objects.get(phone=request.data['phone'])
        except:
            user = None
        if user:
            messageSend = True
            return Response({'result': True}, status=200)
        else:
            return Response({'result': False}, status=200)


class DeleteAddress(generics.DestroyAPIView):
    serializer_class = UserAdressSerializer
    queryset = UserAddress.objects.filter()


class SetNId(APIView):
    def post(self, request):
        print(request.data)
        try:
            request.user.city_id = request.data.get('city_id')
            request.user.notification_id = request.data.get('n_id')
            request.user.save()
        except:
            pass
        return Response(status=200)

class ChangePassword(APIView):
    def post(self, request):
        print(request.data)
        user = User.objects.get(phone = request.data['phone'])
        result = send_sms(user.phone, True, '"Мясо на углях" пароль: ')
        print(result)
        user.set_password(result['code'])
        user.save()
        return Response(status=200)


class SendCode(APIView):
    def post(self, request):
        print(request.data)
        phone = request.data.get('phone')
        result = {}
        try:
            user = User.objects.get(phone=phone)
            if not user.tg_id:
                result = {'success': False, 'message': 'Телеграм username не привязан к аккаунту<br>Свяжитесь с тех.поддержкой'}
            else:
                code = create_random_string(digits=True, num=6)
                send_tg_mgs(user.tg_id, f'Ваш новый пароль {code}')
                user.set_password(code)
                user.save()
                result = {'success': True, 'message': f'Новый отправлен,<br> проверьте чат с meat_coal_bot'}
        except:
            result = {'success':False,'message':'Пользователь не найден'}

        return Response(result,status=200)

# class ComfirmPhoneStepOne(APIView):
#     def post(self, request):
#         print(request.data)
#         phone = request.data.get('phone')
#         result = {'id': False}
#         url = f'https://smsc.ru/sys/send.php?' \
#               f'login={settings.SMS_LOGIN}' \
#               f'&psw={settings.SMS_PASSWORD}' \
#               f'&phones={phone}' \
#               f'&mes=code' \
#               f'&call=1' \
#               f'$fmt=3'
#         response = requests.post(url)
#         print('send sms', response.text)
#
#
#         if 'ERROR' not in response.text:
#             print('send sms', response.text)
#             code = response.text.split(',')[2].split('-')[1].lstrip()
#             result = {'id': code}
#         return Response(result,status=200)


class UsePromo(APIView):
    def post(self, request):
        user = request.user
        code = request.data.get('code')
        try:
            promo = Promo.objects.get(code=code)
            # user.promo = promo
            # user.save()
            if promo.is_only_for_registered and not user.is_authenticated:
                print('promo.is_only_for_registered and not user.is_authenticated')
                return Response({'status': False}, status=200)

            if promo.is_only_for_registered:
                print('promo.is_only_for_registered')
                used_promo_qs = PromoUsed.objects.filter(user=user, promo=promo)
                if used_promo_qs.exists():
                    return Response({'status': False}, status=200)
                else:
                    PromoUsed.objects.create(user=user, promo=promo)

            if promo.uses >= 1:
                promo.uses -= 1
                promo.save()
                return Response({'status': True,'discount':promo.discount}, status=200)
            else:
                return Response({'status': False}, status=200)

        except Promo.DoesNotExist:
            return Response({'status':False},status=200)


class AddAddress(APIView):
    def post(self, request):
        user = request.user
        print(request.data)
        UserAddress.objects.create(user=user,
                                   street=request.data.get('street'),
                                   house=request.data.get('house'),
                                   flat=request.data.get('flat'),
                                   podezd=request.data.get('podezd'),
                                   code=request.data.get('code'),
                                   floor=request.data.get('floor'),
                                   )
        return Response(status=200)

class LandingMail(APIView):
    def post(self,request):
        from django.core.mail import send_mail
        from django.template.loader import render_to_string


        name = json.loads(request.data.get('name'))
        phone = json.loads(request.data.get('phone'))
        msg_html = render_to_string('test.html', {'name': name,
                                                  'phone': phone}
                                    )
        send_mail('Заполнена форма', None, 'info@pandiga.ru', ('stroymir63samara@yandex.ru',),
                  fail_silently=False, html_message=msg_html)
        return Response(status=200)