# Generated by Django 5.0.6 on 2024-08-04 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p1', '0027_query_single'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]