from django.db import models



class OrderItem(models.Model):
    content = models.TextField(blank=True, null=True)


class Order(models.Model):
    cart = models.ForeignKey('cart.Cart', on_delete=models.SET_NULL,null=True,blank=True)
    city = models.ForeignKey('items.City', on_delete=models.SET_NULL,null=True,blank=True)
    order_code = models.CharField(max_length=255, null=True, blank=True)
    client = models.ForeignKey('user.User', blank=True, null=True, default=None, on_delete=models.CASCADE,
                               verbose_name='Заказ клиента')
    guest = models.ForeignKey('user.Guest', blank=True, null=True, default=None, on_delete=models.CASCADE,
                              verbose_name='Заказ гостя')

    items = models.ManyToManyField(OrderItem, blank=True, verbose_name='Товары')
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    payment = models.CharField(max_length=255, null=True, blank=True)
    cafe_address = models.CharField(max_length=255, null=True, blank=True)
    delivery_type = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    need_callback = models.BooleanField(default=False)
    no_cashback = models.BooleanField(default=True)
    persons = models.IntegerField(default=1)
    comment = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    price = models.IntegerField(default=0)
    bonuses = models.IntegerField(default=0)
    promo = models.IntegerField(default=0)
    cashback = models.IntegerField(default=0, blank=True, null=True)

    street = models.CharField(max_length=50, blank=True, null=True)
    house = models.CharField(max_length=50, blank=True, null=True)
    flat = models.CharField(max_length=50, blank=True, null=True)
    podezd = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    floor = models.CharField(max_length=50, blank=True, null=True)

    order_content = models.TextField(blank=True,null=True,default='')
    is_payed = models.BooleanField(default=True)
    is_apply_promo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.client:
            return f'{self.created_at} |  Заказ клиента на сумму: {self.price}'
        else:
            return f'{self.created_at} | Заказ гостя на сумму: {self.price}'

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Payment(models.Model):
    sberId = models.CharField(max_length=255, null=True, blank=True)
    order = models.ForeignKey(Order,
                              blank=True,
                              null=True,
                              default=None,
                              on_delete=models.CASCADE,
                              verbose_name='Заказ',
                              related_name='order_payment')
    status = models.BooleanField(default=False)
    amount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)



