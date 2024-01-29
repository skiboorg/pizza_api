from django.template.loader import render_to_string
from items.models import ItemPrice,SoucePrice,AdditionalIngridientPrice
import settings

import logging
from user.services import send_tg_mgs, send_telegramm_notify
logger = logging.getLogger('django', )

def print_log(text):
    logger.info('--------------------------------------------')
    logger.info(f'{text}')
    logger.info('---------------------------------------------')

def generate_pdf(order,cart):
    from cart.services import erase_cart
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
    data = {
                                'order_code': order.order_code,
                                'price': order.price,
                                'persons': order.persons,
                                'delivery_type': order.delivery_type,
                                'name': order.name,
                                'phone': order.phone,
                                'phone_raw': order.phone_raw,
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
                                'souses':souses,
                                'is_apply_promo':order.cart.is_apply_promo,
                                'bonuses':order.bonuses,

                            }
    html = render_to_string('order.html',
                            {
                                'order_code': order.order_code,
                                'price': order.price,
                                'persons': order.persons,
                                'delivery_type': order.delivery_type,
                                'name': order.name,
                                'phone': order.phone,
                                'phone_raw': order.phone_raw,
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
                                'souses':souses,
                                'is_apply_promo':order.cart.is_apply_promo,
                                'bonuses':order.bonuses,

                            })
    #pdf = pydf.generate_pdf(html)
    filename = f'media/orders/{order.order_code}.html'
    with open(filename, mode= 'w+') as f:
        f.write(str(html))
    order.file = f'orders/{order.order_code}.html'

    for i in items:
        order.order_content += f'{i}<br>'
    order.order_content += '<br>'
    for i in souses:
        order.order_content += f'{i}<br>'
    order.save()
    print_log(f'save order {order.order_code} items {order.order_content}')
    # ----------------- uncomment
    print(data)

    send_telegramm_notify(f'Новый заказ {order.order_code}. https://meat-coal.ru/media/orders/{order.order_code}.html',order.city.tg_chat_id)

    if order.client and order.client.tg_id:
        send_tg_mgs(order.client.tg_id,f'Ваш заказ принят. Номер заказа: {order.order_code}')

    print_log(f'order {order.order_code} erase cart')
    erase_cart(cart)

