# Generated by Django 5.0.6 on 2024-07-25 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p1', '0004_alter_category_rank'),
    ]

    operations = [
        migrations.CreateModel(
            name='Random',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('image', models.ImageField(default='default/logo.png', upload_to='random/')),
            ],
        ),
    ]