from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, phone, password, **extra_fields):
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)

class Promo(models.Model):

    code = models.CharField('Промокод',max_length=50, blank=True, null=True)
    discount = models.IntegerField('% скидки',default=0)
    uses = models.IntegerField('Кол-во использований',default=0)


class User(AbstractUser):

    username = None
    first_name = None
    last_name = None
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE, blank=True, null=True)
    session = models.CharField('Ключ сессии', max_length=255, blank=True, null=True)
    email = models.EmailField('Эл. почта',blank=True,null=True, unique=True)
    fio = models.CharField('ФИО', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True,unique=True)
    profile_ok = models.BooleanField(default=False)
    birthday = models.DateField('Д/Р', blank=True, null=True)
    bonuses = models.IntegerField(default=0)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'Аккаунт. ID {self.id}, Дата регистрации: {self.date_joined} | {self.phone}'


class Guest(models.Model):
    session = models.CharField('Ключ сессии', max_length=255, blank=True, null=True)
    email = models.EmailField('Эл. почта', blank=True, null=True)
    fio = models.CharField('ФИО', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)



    def __str__(self):
        return f'Гостевой аккаунт. ID {self.id}'


class UserAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='addresses')
    street = models.CharField( max_length=50, blank=True, null=True)
    house = models.CharField( max_length=50, blank=True, null=True)
    flat = models.CharField( max_length=50, blank=True, null=True)
    podezd = models.CharField( max_length=50, blank=True, null=True)
    code = models.CharField( max_length=50, blank=True, null=True)
    floor = models.CharField( max_length=50, blank=True, null=True)


