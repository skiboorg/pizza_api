# Generated by Django 3.1.5 on 2021-05-13 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20210210_1556'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='uses',
            field=models.IntegerField(default=0, verbose_name='Кол-во использований'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Промокод'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='discount',
            field=models.IntegerField(default=0, verbose_name='% скидки'),
        ),
    ]
