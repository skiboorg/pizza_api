# Generated by Django 3.1.5 on 2021-04-19 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0019_item_is_show_at_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='is_show_at_index',
        ),
    ]
