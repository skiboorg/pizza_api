# Generated by Django 3.1.5 on 2021-11-19 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_auto_20210914_1525'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]