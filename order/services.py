import pydf
import requests
from django.template.loader import render_to_string
from items.models import ItemPrice,SoucePrice,AdditionalIngridientPrice
import settings
from django.core.mail import send_mail,EmailMessage
from cart.services import erase_cart
from pyfcm import FCMNotification

def generate_pdf(order,cart):
    items = []
    constructors = []
    souses = []
    all_cart_items = cart.items.all()
    all_cart_constructors = cart.pizza_constructors.all()
    all_cart_souses = cart.souces.all()
    for i in all_cart_items:
        item=''
        if i.item.category.is_pizza:
            item_prices = ItemPrice.objects.get(city=i.city, item=i.item)
            if i.selected_size == 33:
                item_price = item_prices.price_33
            else:
                item_price = item_prices.price
            item += f'Пицца - {i.item.name} {i.quantity}шт {28 if i.selected_size== 22 else 33}см {i.quantity * item_price}руб '
        else:
            item_price = ItemPrice.objects.get(city=i.city, item=i.item)
            if i.item.category.is_meat:
                item += f'{i.item.category.name} - {i.item.name} {i.quantity * i.item.min_unit}{i.item.unit_name} {i.quantity * item_price.price}руб'
            else:
                item += f'{i.item.category.name} - {i.item.name} {i.quantity}шт  {i.quantity * item_price.price}руб'

        if i.item.category.is_pizza:
            for b_i in i.base_ingridients.all():
                if b_i.is_removed: #not
                    item += f'Убрано - {b_i.item.name}, '
            for a_i in i.additional_ingridients.all():
                if a_i.is_added:
                    item_price = AdditionalIngridientPrice.objects.get(city=i.city, ingridient=a_i.item)
                    item += f'Добавлено - {a_i.item.name} ({item_price.price}руб), '
        items.append(item)
    for i in all_cart_constructors:
        constructor = ''
        text = ''
        for i_p in i.items.all():
            text += f'{i_p.name}'
        constructor += f'Конструктор - {text} {i.quantity}шт {i.quantity * i.price}руб'
        constructors.append(constructor)
    for i in all_cart_souses:
        item_price = SoucePrice.objects.get(city=i.city, item=i.item)
        souses.append(f'Соус  - {i.item.name} {i.quantity}шт {i.quantity * item_price.price}руб')
    html = render_to_string('order.html',
                            {
                                'order_code': order.order_code,
                                'price': order.price,
                                'persons': order.persons,
                                'delivery_type': order.delivery_type,
                                'name': order.name,
                                'phone': order.phone,
                                'street': order.street,
                                'house': order.house,
                                'flat': order.flat,
                                'podezd': order.podezd,
                                'code': order.code,
                                'floor': order.floor,
                                'payment': order.payment,
                                'need_callback': order.need_callback,
                                'no_cashback': order.no_cashback,
                                'cashback': order.cashback,
                                'time': order.time,
                                'date': order.date,
                                'cafe_address': order.cafe_address,
                                'comment': order.comment,
                                'items':items,
                                'constructors':constructors,
                                'souses':souses

                            })
    # pdf = pydf.generate_pdf(html)
    # filename = f'orders/{order.order_code}.pdf'
    # with open(filename, mode= 'wb') as f:
    #     f.write(pdf)
    # send_email(filename,order)

    send_mail('Новый заказ', None, settings.MAIL_TO, (order.city.order_email,),
              fail_silently=False, html_message=html)
    url = f'https://smsc.ru/sys/send.php?login={settings.SMS_LOGIN}&psw={settings.SMS_PASSWORD}&phones={order.phone}&mes=Мясо на углях: Номер заказа {order.order_code}'
    response1 = requests.post(url)
    if order.client:
        if order.client.notification_id:

            push_service = FCMNotification(api_key=settings.FCM_API_KEY)

            registration_id = order.client.notification_id
            message_title = "Ваш заказ"
            message_body = f'Номер заказа {order.order_code}'

            data_message = {

            }

            result = push_service.notify_single_device(registration_id=registration_id,
                                                       sound='Default',
                                                       message_title=message_title,
                                                       message_body=message_body,
                                                       data_message=data_message,
                                                       )
            print(result)
        else:
            url1 = f'https://smsc.ru/sys/send.php?login={settings.SMS_LOGIN}&psw={settings.SMS_PASSWORD}&phones={order.city.order_phone}&mes=Новый заказ №{order.order_code}'
            response2 = requests.post(url1)
    else:
        url1 = f'https://smsc.ru/sys/send.php?login={settings.SMS_LOGIN}&psw={settings.SMS_PASSWORD}&phones={order.city.order_phone}&mes=Новый заказ №{order.order_code}'
        response2 = requests.post(url1)

    erase_cart(cart)


def send_email(filename,order):
    url = f'https://smsc.ru/sys/send.php?login={settings.SMS_LOGIN}&psw={settings.SMS_PASSWORD}&phones={order.phone}&mes=Мясо на углях: Номер заказа {order.order_code}'
    response = requests.post(url)
    print(response.text)
    mail = EmailMessage('Новый заказ', 'Новый заказ', settings.MAIL_TO, (settings.MAIL_TO,))
    # mail.attach(file.name, file.read(), file.content_type)
    mail.attach_file(filename)
    mail.send()
