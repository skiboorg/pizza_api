import pydf
from django.template.loader import render_to_string
from items.models import ItemPrice,SoucePrice,AdditionalIngridientPrice

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
            item += f'Пицца - {i.item.name} {i.quantity}шт {i.selected_size}см {i.quantity * item_price}руб '
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
    pdf = pydf.generate_pdf(html)
    with open(f'orders/{order.order_code}.pdf', mode= 'wb') as f:
        f.write(pdf)