# Generated by Django 5.0.6 on 2024-06-13 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('d1', '0003_meat_kebap_delete_article_delete_publication'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Souce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, null=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='kebap',
            name='salat',
            field=models.ManyToManyField(to='d1.salat'),
        ),
        migrations.AddField(
            model_name='kebap',
            name='souce',
            field=models.ManyToManyField(to='d1.souce'),
        ),
    ]