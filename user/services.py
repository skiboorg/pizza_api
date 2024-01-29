import json
from random import choices
import string
import requests
import settings
from .models import User
from pyfcm import FCMNotification

def create_random_string(digits=False, num=4):
    if not digits:
        random_string = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=num))
    else:
        random_string = ''.join(choices(string.digits, k=num))
    return random_string

def set_user_rating(id,value):
    """Обновление рейтинга техники при создании отзыва"""
    from .models import User

    user = User.objects.get(id=id)
    user.rate_times += 1
    user.rate_value += value
    user.rating = round(user.rate_value / user.rate_times)
    user.save()
    return


def send_sms(phone, is_code=False, text=''):
    sms_text = text
    result = {'code':False}
    code = ''
    if is_code:
        code = ''.join(choices(string.digits, k=4))
        sms_text = text + code
    url = f'https://smsc.ru/sys/send.php?login={settings.SMS_LOGIN}&' \
          f'psw={settings.SMS_PASSWORD}&' \
          f'phones={phone}&' \
          f'mes={sms_text}&' \
          f'sender=kafeMyasoug'
    response = requests.post(url)
    print('send sms', response.text)
    if 'ERROR' not in response.text:
        result = {'code':code}
    return result


def sendPush(send_to,mode, title, text, n_id=None, url=None, city=None):
    push_service = ''
    if send_to == 'client':
        push_service = FCMNotification(api_key=settings.FCM_API_KEY)
    if send_to == 'courier':
        push_service = FCMNotification(api_key=settings.COURIER_FCM_API_KEY)

    registration_id = n_id
    message_title = title
    message_body = text

    data_message = {
        "url": url
    }
    if mode == 'single':
        result = push_service.notify_single_device(registration_id=registration_id,
                                                   sound='default',
                                                   message_title=message_title,
                                                   message_body=message_body,
                                                   )
        print(result)
    if mode == 'promo':
        registration_ids = []
        if city:
            all_users = User.objects.filter(city=city)
        else:
            all_users = User.objects.all()
        for user in all_users:
            if user.notification_id:
                registration_ids.append(user.notification_id)
        print(registration_ids)

        result = push_service.notify_multiple_devices(registration_ids=registration_ids,
                                                   sound='default',
                                                   message_title=message_title,
                                                   message_body=message_body,
                                                   data_message=data_message,
                                                   )
        print(result)


def send_telegramm_notify(text,chat_id):
    response = requests.get(f'https://api.telegram.org/bot{settings.TG_BOT_TOKEN}/sendMessage?chat_id={chat_id}&'
                            f'text={text}')
    print(response.text)
    return

def send_tg_mgs(to_id,message):
    Headers = { 'Content-Type':'application/json'}
    data = {
        "chat_id":to_id,
        "message":message
    }
    res = requests.post('http://0.0.0.0:5000/send_message',headers=Headers,data=json.dumps(data))
    print(res)