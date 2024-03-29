# Generated by Django 3.1.5 on 2021-08-17 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('promotion', '0005_auto_20210726_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='is_first_order',
            field=models.BooleanField(default=False, verbose_name='Скидка на первый заказ?'),
        ),
        migrations.CreateModel(
            name='PromotionUse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='promotion.promotion')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
