# Generated by Django 3.1.5 on 2021-07-25 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0003_promotion_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='is_need_notify',
            field=models.BooleanField(default=False, verbose_name='Сделать расслку пушей после сохранения акции?'),
        ),
    ]
