# Generated by Django 3.1.5 on 2022-03-20 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_order_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_new',
            field=models.BooleanField(default=False),
        ),
    ]
