from user.models import Guest
from .models import *
from items.models import Item
from items.models import City, ItemPrice, AdditionalIngridientPrice
import settings
import uuid


def check_if_guest_exists(session_id):
    guest, created = Guest.objects.get_or_create(session=session_id)
    if created:
        print('guest created')
    else:
        print('guest already created')
    return guest


def check_if_cart_exists(request, session_id):
    user = None
    guest = None
    if request.user.is_authenticated:
        user = request.user
    else:
        guest = check_if_guest_exists(session_id)

    if user:
        cart, created = Cart.objects.get_or_create(client=user)
    else:
        cart, created = Cart.objects.get_or_create(guest=guest)

    if created:
        print('new cart created')
    else:
        print('cart already created')
    return cart

def create_hash(cart, data):
    user = cart.client
    guest = cart.guest

    if user:
        session_id = user.session
    if guest:
        session_id = guest.session

    item = data.get('item')
    selected_size = data.get('selected_size')
    base_ingridients = item.get('base_ingridients')
    additional_ingridients = item.get('additional_ingridients')
    weight = data.get('weight')
    units = data.get('units')
    is_meat = data.get('is_meat')
    b_i_summ=''
    a_i_summ=''
    code =item.get('code')

    if not is_meat:
        # added
        try:
            for b_i in base_ingridients:
                if b_i.get("is_removed"):
                    b_i_summ += f'{b_i.get("code") }'

            for a_i in additional_ingridients:
                if a_i.get("is_added"):
                    a_i_summ += f'{a_i.get("code") }'
        except:
            pass


    # total_summ = f"{item.get('id')+ item.get('category').get('id') + selected_size + weight}-{a_i_summ}-{b_i_summ}" #+ units
    total_summ = f"{item.get('id')+ selected_size + weight}-{a_i_summ}-{b_i_summ}" #+ units

    return f'{session_id}_{total_summ}{code}'


def add_to_cart(cart,data):
    user = cart.client
    guest = cart.guest

    is_added = False
    is_created = False

    print (data)

    item = data.get('item')
    selected_size = data.get('selected_size')
    base_ingridients = item.get('base_ingridients')
    additional_ingridients = item.get('additional_ingridients')
    weight = data.get('weight')
    units = data.get('units')
    city_id = data.get('city_id')
    is_meat = data.get('is_meat')
    item_id = item.get('id')

    item_code = create_hash(cart, data)

    city = City.objects.get(id=city_id)
    item_prices = ItemPrice.objects.get(city=city, item_id=item_id)
    if selected_size == 33:
        item_price = item_prices.price_33
    else:
        item_price = item_prices.price

    print('item_price',item_price)
    print('selected_size',selected_size)


    if item:
        if user:
            print('adding for user')
            try:
                cart_item = CartItem.objects.get(code=item_code)
                print('item found', cart_item)
                cart_item.quantity += units
                cart_item.price_per_unit = item_price
                cart_item.price = cart_item.quantity * item_price
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(client=user,
                                                    item_id=item_id,
                                                    selected_size=selected_size,
                                                    weight=weight,
                                                    quantity=units,
                                                    code=item_code,
                                                    city=city,
                                                    price_per_unit=item_price,
                                                    price=item_price * units,
                                                    bonuses=item_price * settings.BONUS_PERCENT
                                                    )
                print(cart_item)
                print('item found', cart_item)
                is_created = True
        if guest:
            try:
                cart_item = CartItem.objects.get(code=item_code)

                cart_item.quantity += units
                cart_item.price_per_unit = item_price
                cart_item.price = cart_item.quantity * item_price
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(guest=guest,
                                                    item_id=item_id,
                                                    selected_size=selected_size,
                                                    weight=weight,
                                                    quantity=units,
                                                    code=item_code,
                                                    city=city,
                                                    price_per_unit=item_price,
                                                    price=item_price*units,
                                                    bonuses=item_price * settings.BONUS_PERCENT
                                                    )
                is_created = True

    if is_created and not is_meat:
        # added
        try:
            for i in base_ingridients:
                base_ingridient = CartItemBaseIngrigient.objects.create(item_id=i.get('id'),is_removed=i.get('is_removed'))
                cart_item.base_ingridients.add(base_ingridient)

            for i in additional_ingridients:
                additional_ingridient = CartItemAdditionalIngrigient.objects.create(item_id=i.get('id'),is_added=i.get('is_added'))
                cart_item.additional_ingridients.add(additional_ingridient)

                if i.get('is_added'):
                    is_added = True
                    additional_ingridient_price = AdditionalIngridientPrice.objects.get(city=city, ingridient_id=i.get('id'))
                    cart_item.ingridients_price += additional_ingridient_price.price
                    cart_item.price += additional_ingridient_price.price
                    cart_item.price_per_unit += additional_ingridient_price.price
                    cart_item.bonuses += additional_ingridient_price.price * settings.BONUS_PERCENT
        except:
            pass

        if is_added:
            cart_item.save()
        cart.items.add(cart_item)

    if is_meat:
        cart.items.add(cart_item)
        print(additional_ingridients)
    calculate_total_cart_price(cart)


def remove_cart_item(item):
    for b_i in item.base_ingridients.all():
        b_i.delete()
    for a_i in item.additional_ingridients.all():
        a_i.delete()
    item.delete()


def erase_cart(cart):
    all_cart_items = cart.items.all()
    for i in all_cart_items:
        remove_cart_item(i)
    all_cart_constructors = cart.pizza_constructors.all()
    for i in all_cart_constructors:
        i.delete()
    all_cart_souses = cart.souces.all()
    for i in all_cart_souses:
        i.delete()
    cart.total_price = 0
    cart.total_bonuses = 0
    cart.save()

def calculate_total_cart_price(cart):
    all_cart_items = cart.items.all()
    all_cart_constructors = cart.pizza_constructors.all()
    all_cart_souses = cart.souces.all()
    cart.total_price = 0
    cart.total_bonuses = 0
    for i in all_cart_items:
        cart.total_price += i.price
        cart.total_bonuses += i.bonuses
    for i in all_cart_constructors:
        cart.total_price += i.price
        cart.total_bonuses += i.bonuses
    for i in all_cart_souses:
        cart.total_price += i.price
        cart.total_bonuses += i.bonuses
    cart.save()

    items_price = 0

    for i in all_cart_items:

        if i.item.category.id == 2:
            items_price+=i.price

    print(items_price)

    if items_price >= 2400:
        gift = Item.objects.filter(is_gift=True)
        for g in gift:
            item_in = False
            for i in all_cart_items:
                if i.item == g:
                    print('gift in')
                    item_in = True
                    break
            if not item_in:
                new_item = CartItem.objects.create(item=g,price=0,units=1,city_id=1,price_per_unit=0,quantity=1,code=uuid.uuid4())
                cart.items.add(new_item)
                print('gift created')

            print('more2000')
    else:
        gift = Item.objects.filter(is_gift=True)
        for g in gift:
            for i in all_cart_items:
                if i.item == g:
                    i.delete()
                    cart.items.remove(i)
            print('less2000')

