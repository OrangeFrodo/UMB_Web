# Generated by Django 3.1.3 on 2021-02-05 00:04

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0031_customer_mobile_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='mobile_num',
        ),
        migrations.AddField(
            model_name='customer',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, unique=True),
        ),
    ]