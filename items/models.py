from django.db import models
from pytils.translit import slugify
from django.utils.safestring import mark_safe
from random import choices
import string
from ckeditor_uploader.fields import RichTextUploadingField




class City(models.Model):
    name = models.CharField('Город', max_length=255, blank=False, null=True)
    info = models.CharField('Информация о достаке',max_length=255, blank=True, null=True)
    is_main = models.BooleanField('Это город по умолчанию?', default=False)
    order_email = models.CharField('Email для отправки заказа', max_length=255, blank=False, null=True)
    order_phone = models.CharField('Телефон для отправки заказа', max_length=255, blank=False, null=True)
    domain = models.CharField('Домен', max_length=255, blank=False, null=True, default='')
    sber_login = models.CharField('Логин сбре', max_length=255, blank=False, null=True, default='')
    sber_pass = models.CharField('Пароль сбер', max_length=255, blank=False, null=True, default='')
    sber_url = models.CharField('Сбер URL', max_length=255, blank=False, null=True, default='')

    main_phone = models.CharField('Телефон в шапке', max_length=255, blank=False, null=True)
    contacts_text = RichTextUploadingField('Тект для страницы контакты', blank=True, null=True)
    payment_text = RichTextUploadingField('Тект для опллаты', blank=True, null=True)
    delivery_times = models.CharField('ДОСТАВКА РАБОТАЕТ', max_length=255, blank=False, null=True)
    delivery_from_price = models.CharField('СУММА ЗАКАЗА', max_length=255, blank=False, null=True)
    delivery_price = models.CharField('ЦЕНА ДОСТАВКИ', max_length=255, blank=False, null=True)
    delivery_time = models.CharField('ВРЕМЯ ДОСТАВКИ', max_length=255, blank=False, null=True)
    about_image = models.ImageField('Главное изображение на странице о нас', upload_to='city/', blank=True)
    about_kitchen = models.ImageField('Изображение кухни на странице о нас', upload_to='city/', blank=True)
    is_show_peoples = models.BooleanField('Отображать поваров', default=False)
    about_p9_text = models.TextField('Текст пункта 9', null= True, blank=True)
    vk_link = models.CharField('Vk', max_length=255, blank=True, null=True)
    inst_link = models.CharField('Instagram', max_length=255, blank=True, null=True)
    policy_text = RichTextUploadingField('Тект политики', blank=True, null=True)
    rules_text = RichTextUploadingField('Тект правил', blank=True, null=True)


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"

class Banners(models.Model):
    order_num = models.IntegerField("Номер по порядку", default=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Город')
    image = models.ImageField('Изображение', upload_to='banners/', blank=False)
    is_active = models.BooleanField('Показывать баннер?', default=True)

    def __str__(self):
        return f'Баннер {self.id} номер по порядку {self.order_num}'

    class Meta:
        ordering = ('-order_num',)
        verbose_name = "Баннеры"
        verbose_name_plural = "Баннер"


class CafeAddress(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=False, null=True,
                             verbose_name='Город', related_name='adresses')
    address = models.TextField('Адрес кафе', max_length=255, blank=True, null=True)
    coordinates = models.CharField('Координаты', max_length=255, blank=False, null=True)
    phone = models.CharField('Телефон', max_length=255, blank=False, null=True)

    def __str__(self):
        return f'{self.city.name} - {self.address}'

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"


class Category(models.Model):
    order_num = models.IntegerField('Порядок вывода', default=100)
    city = models.ManyToManyField(City, verbose_name='Категория доступна в городах',
                                  blank=True, db_index=True)
    name = models.CharField('Название категории', max_length=255, blank=True, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, editable=False)
    is_pizza = models.BooleanField('Это пицца?', default=False)
    is_meat = models.BooleanField('Это шашлык?', default=False)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('order_num',)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class BaseIngridient(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField('Базовый ингридиент', max_length=255, blank=True, null=True)
    is_for_pizza = models.BooleanField('Для пиццы?', default=False)
    is_for_meat = models.BooleanField('Для шашлыка?', default=False)
    is_can_removed = models.BooleanField('Может быть удален?', default=False)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)
        verbose_name = "Базовый ингридиент"
        verbose_name_plural = "Базовые ингридиенты"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=8))
        super(BaseIngridient, self).save(*args, **kwargs)


class AdditionalIngridient(models.Model):
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField('Дополнительный ингридиент', max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='items/ingridients/', blank=True)
    is_for_pizza = models.BooleanField('Для пиццы?', default=False)
    is_for_meat = models.BooleanField('Для шашлыка?', default=False)
    is_added = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Дополнительный ингридиент"
        verbose_name_plural = "Дополнительные ингридиенты"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=8))
        super(AdditionalIngridient, self).save(*args, **kwargs)


class AdditionalIngridientPrice(models.Model):
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE, blank=False, null=True,
                             db_index=True)
    ingridient = models.ForeignKey(AdditionalIngridient, verbose_name='Дополнительный ингридиент',
                                   on_delete=models.CASCADE, blank=False, null=True, db_index=True,related_name='price')
    price = models.IntegerField('Цена', blank=False, null=True)

    def __str__(self):
        return f'{self.city.name} {self.ingridient.name} {self.price}'

    class Meta:
        verbose_name = "Цена на дополнительный ингридиент"
        verbose_name_plural = "Цены на дополнительные ингридиенты"


class Souce(models.Model):
    name = models.CharField('Название соуса', max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='items/', blank=False)
    city = models.ManyToManyField(City, verbose_name='Соус доступен в городах',
                             blank=True, db_index=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Соус"
        verbose_name_plural = "Соусы"


class SoucePrice(models.Model):
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE, blank=False, null=True,
                             db_index=True)
    item = models.ForeignKey(Souce, verbose_name='Товар', on_delete=models.CASCADE, blank=False, null=True,
                             db_index=True, related_name='prices')
    price = models.IntegerField('Цена', blank=False, null=True)

    def __str__(self):
        return f'{self.city.name} {self.item.name} {self.price}'

    class Meta:
        verbose_name = "Цена на соус"
        verbose_name_plural = "Цены на соусы"


class Item(models.Model):
    order_num = models.IntegerField(default=100)
    code = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category,blank=False,null=True,on_delete=models.SET_NULL,
                                 verbose_name='Категория',related_name='items')
    name = models.CharField('Название товара', max_length=255, blank=True, null=True)
    image = models.ImageField('Изображение', upload_to='items/', blank=False)


    city = models.ManyToManyField(City, verbose_name='Продукт доступен в городах',
                             blank=True, db_index=True)
    base_ingridients = models.ManyToManyField(BaseIngridient, verbose_name='Базовые ингридиенты', blank=True)
    additional_ingridients = models.ManyToManyField(AdditionalIngridient, verbose_name='Дополнительные ингридиенты',
                                                    blank=True)

    unit_name = models.CharField('Еденица изверения товара', max_length=255, blank=True, null=True)
    min_unit = models.IntegerField('Минимальное количество', blank=False, null=True, editable=True)

    discount = models.IntegerField('Скидка', default=0)

    weight = models.IntegerField('Вес (для пиццы это вес 28см)', default=0)
    weight_33 = models.IntegerField('Вес для пиццы 33см)', default=0)
    callories = models.IntegerField('Калорий', default=0)
    fat = models.IntegerField('Жиры', default=0)
    belki = models.IntegerField('Белки', default=0)
    uglevod = models.IntegerField('Углеводы', default=0)

    is_recommended = models.BooleanField('Рекомендуемый товар?', default=False, db_index=True)
    is_for_meat = models.BooleanField('Рекомендуемый товар для шашлыка?', default=False, db_index=True)
    is_new = models.BooleanField('Товар новинка ?', default=False, db_index=True)
    is_gift = models.BooleanField('Товар подарок ?', default=False, db_index=True)

    is_active = models.BooleanField('Отображать ?', default=True, db_index=True)

    buys = models.IntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="100" />'.format(self.image.url))

    image_tag.short_description = 'Картинка'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = '-' + ''.join(choices(string.ascii_lowercase + string.digits, k=8))
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.min_unit} {self.unit_name}'

    class Meta:
        ordering = ('order_num',)
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ItemPrice(models.Model):
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE, blank=False, null=True,
                             db_index=True)
    item = models.ForeignKey(Item, verbose_name='Товар', on_delete=models.CASCADE, blank=False, null=True,
                             db_index=True, related_name='prices')

    old_price = models.IntegerField( default=0)
    old_price_33 = models.IntegerField( default=0)
    price = models.IntegerField('Цена (если пицца то для размера 28см)', blank=False, null=True)
    price_33 = models.IntegerField('Цена для пиццы 33см', default=0)

    def __str__(self):
        return f'{self.city.name} {self.item.name} {self.price}'

    class Meta:
        verbose_name = "Цена на товар"
        verbose_name_plural = "Цены на товары"



