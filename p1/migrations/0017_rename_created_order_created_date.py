# Generated by Django 5.0.6 on 2024-07-30 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('p1', '0016_order_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='created',
            new_name='created_date',
        ),
    ]
