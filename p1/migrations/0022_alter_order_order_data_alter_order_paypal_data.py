# Generated by Django 5.0.6 on 2024-08-01 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p1', '0021_alter_product_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_data',
            field=models.TextField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='paypal_data',
            field=models.TextField(blank=True, editable=False, null=True),
        ),
    ]