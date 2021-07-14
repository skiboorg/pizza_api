# Generated by Django 3.1.5 on 2021-07-11 11:38

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0021_auto_20210711_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='banners',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='items.city', verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='city',
            name='contacts_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Тект для страницы контакты'),
        ),
        migrations.AlterField(
            model_name='city',
            name='payment_text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Тект для опллаты'),
        ),
    ]