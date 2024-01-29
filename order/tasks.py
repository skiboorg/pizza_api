from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
import settings
from .models import Order
from datetime import timedelta
from django.utils import timezone
@shared_task
def remove_orders():
    orders = Order.objects.filter(created_at__lt=timezone.now() - timedelta(days=7))
    orders.delete()
