from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
import settings

@shared_task
def send_email(title,to,template,data):
    msg_html = render_to_string(template, data)
    send_mail(title, None, settings.YA_USER, [to],
              fail_silently=False, html_message=msg_html)