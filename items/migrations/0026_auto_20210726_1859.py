# Generated by Django 3.1.5 on 2021-07-26 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0025_auto_20210725_1759'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('order_num', 'is_gift'), 'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
    ]