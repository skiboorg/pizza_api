# Generated by Django 3.1.5 on 2021-02-25 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_city_coordinates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='address',
        ),
        migrations.RemoveField(
            model_name='city',
            name='coordinates',
        ),
        migrations.CreateModel(
            name='CafeAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(blank=True, max_length=255, null=True, verbose_name='Адрес кафе')),
                ('coordinates', models.CharField(max_length=255, null=True, verbose_name='Координаты')),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='adresses', to='items.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
            },
        ),
    ]
