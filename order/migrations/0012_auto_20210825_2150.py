# Generated by Django 3.1.5 on 2021-08-25 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_order_is_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_delivery_in_progress',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_payed',
            field=models.BooleanField(default=False),
        ),
    ]
