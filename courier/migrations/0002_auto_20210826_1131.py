# Generated by Django 3.1.5 on 2021-08-26 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courier', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courier',
            old_name='fio',
            new_name='label',
        ),
    ]
