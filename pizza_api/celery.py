import os
import settings
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizza_api.settings')

app = Celery('webilang_api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


