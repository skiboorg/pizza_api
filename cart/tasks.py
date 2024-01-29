from celery import shared_task
from .models import *
from user.models import Guest
import settings

@shared_task
def remove_guests():
    items = Guest.objects.all()
    items.delete()

    items = Cart.objects.all()
    items.delete()

    items = CartItemBaseIngrigient.objects.all()
    items.delete()
    items = CartItemAdditionalIngrigient.objects.all()
    items.delete()
