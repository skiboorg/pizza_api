import os
import settings
from celery import Celery

from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizza_api.settings')

app = Celery('pizza_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'remove_guests': {
            'task': 'cart.tasks.remove_guests',
            'schedule': crontab(minute=0, hour=0)
       },
    'remove_orders': {
            'task': 'order.tasks.remove_orders',
            'schedule': crontab(minute=0, hour=1)
       },
}