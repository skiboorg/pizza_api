# Generated by Django 4.2.1 on 2023-12-16 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0031_city_shopid'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='secretKey',
            field=models.CharField(max_length=255, null=True),
        ),
    ]