# Generated by Django 3.1.5 on 2021-07-13 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20210513_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notification_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='ID для сообщений'),
        ),
    ]
