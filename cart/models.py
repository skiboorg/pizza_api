from django.db import models


class CartItemBaseIngrigient(models.Model):
    item = models.ForeignKey('items.BaseIngridient', blank=True, null=True, on_delete=models.CASCADE)
    is_removed = models.BooleanField(blank=True, null=True)


class CartItemAdditionalIngrigient(models.Model):
    item = models.ForeignKey('items.AdditionalIngridient', blank=True, null=True, on_delete=models.CASCADE)
    is_added = models.BooleanField(blank=True, null=True)


class CartItem(models.Model):
    code = models.CharField(max_length=255,blank=False,null=True, unique=True)
    client = models.ForeignKey('user.User', blank=True, null=True, default=None, on_delete=models.CASCADE)
    guest = models.ForeignKey('user.Guest', blank=True, null=True, default=None, on_delete=models.CASCADE)
    item = models.ForeignKey('items.Item', blank=True, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey('items.City', blank=True, null=True, on_delete=models.CASCADE)
    base_ingridients = models.ManyToManyField(CartItemBaseIngrigient,
                                              verbose_name='Базовые ингридиенты', blank=True)
    additional_ingridients = models.ManyToManyField(CartItemAdditionalIngrigient,
                                                    verbose_name='Дополнительные ингридиенты', blank=True)
    selected_size = models.IntegerField(default=0)

    weight = models.IntegerField(default=0)
    units = models.IntegerField(default=0)
    quantity = models.IntegerField('Кол-во', blank=True, null=True, default=1)
    ingridients_price = models.IntegerField(default=0)
    price_per_unit = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    bonuses = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.item.name} X {self.quantity}'

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзинах"

class CartSouce(models.Model):
    code = models.CharField(max_length=255, blank=False, null=True, unique=True)
    client = models.ForeignKey('user.User', blank=True, null=True, default=None, on_delete=models.CASCADE)
    guest = models.ForeignKey('user.Guest', blank=True, null=True, default=None, on_delete=models.CASCADE)
    city = models.ForeignKey('items.City', blank=True, null=True, on_delete=models.CASCADE)
    item = models.ForeignKey('items.Souce', blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField('Кол-во', blank=True, null=True, default=1)
    price_per_unit = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    bonuses = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.item.name} X {self.quantity}'

    class Meta:
        verbose_name = "Соус в корзине"
        verbose_name_plural = "Соусы в корзинах"


class CartConstructor(models.Model):
    code = models.CharField(max_length=255, blank=False, null=True, unique=True)
    client = models.ForeignKey('user.User', blank=True, null=True, default=None, on_delete=models.CASCADE)
    guest = models.ForeignKey('user.Guest', blank=True, null=True, default=None, on_delete=models.CASCADE)
    city = models.ForeignKey('items.City', blank=True, null=True, on_delete=models.CASCADE)
    items = models.ManyToManyField('items.Item', blank=True, null=True)
    quantity = models.IntegerField('Кол-во', blank=True, null=True, default=1)
    price_per_unit = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    bonuses = models.IntegerField(default=0)

    def __str__(self):
        return f'Конструктор X {self.quantity}'

    class Meta:
        verbose_name = "Конструктор в корзине"
        verbose_name_plural = "Конструкторы в корзинах"


class Cart(models.Model):
    client = models.ForeignKey('user.User', blank=True, null=True, default=None, on_delete=models.CASCADE,
                               verbose_name='Корзина клиента')
    guest = models.ForeignKey('user.Guest', blank=True, null=True, default=None, on_delete=models.CASCADE,
                              verbose_name='Корзина гостя')


    pizza_constructors = models.ManyToManyField(CartConstructor, blank=True,
                                               verbose_name='Собранные пиццы')
    souces = models.ManyToManyField(CartSouce, blank=True,
                                               verbose_name='Соусы')
    items = models.ManyToManyField(CartItem, blank=True, verbose_name='Товары')
    is_apply_promo = models.BooleanField(default=False)

    persons = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)
    total_bonuses = models.IntegerField(default=0)



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.client:
            return f'Корзина клиента : {self.client.id} '
        else:
            return f'Корзина гостя : {self.guest.id} '

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

