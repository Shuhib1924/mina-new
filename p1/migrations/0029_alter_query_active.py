# Generated by Django 5.0.6 on 2024-08-04 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p1', '0028_query_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]