# Generated by Django 3.1.5 on 2021-04-06 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0012_item_is_gift'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemprice',
            name='is_discount',
            field=models.BooleanField(default=False),
        ),
    ]
