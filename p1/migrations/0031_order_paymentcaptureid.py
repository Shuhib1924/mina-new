# Generated by Django 5.0.6 on 2024-08-05 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p1', '0030_rename_form_name_order_form_companyaddress_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paymentCaptureID',
            field=models.CharField(max_length=40, null=True),
        ),
    ]
