# Generated by Django 5.0.6 on 2024-07-27 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('p1', '0008_variation_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='active',
        ),
    ]