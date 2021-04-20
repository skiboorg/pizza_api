# Generated by Django 3.1.5 on 2021-04-19 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0017_itemprice_old_price_33'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='is_for_meat',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Рекомендуемый товар для шашлыка?'),
        ),
        migrations.AlterField(
            model_name='item',
            name='is_recommended',
            field=models.BooleanField(db_index=True, default=False, verbose_name='Рекомендуемый товар?'),
        ),
    ]
