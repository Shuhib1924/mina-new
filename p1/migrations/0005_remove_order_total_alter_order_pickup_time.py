# Generated by Django 5.0.6 on 2024-06-10 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p1', '0004_remove_order_email_order_name_order_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total',
        ),
        migrations.AlterField(
            model_name='order',
            name='pickup_time',
            field=models.TimeField(),
        ),
    ]