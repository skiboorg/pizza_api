# Generated by Django 5.0.1 on 2024-01-25 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0022_alter_order_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='orders/'),
        ),
    ]
