# Generated by Django 3.1.5 on 2021-04-19 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0018_auto_20210419_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_show_at_index',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Отображать на главной странице?'),
        ),
    ]
