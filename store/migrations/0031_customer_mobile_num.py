# Generated by Django 3.1.3 on 2021-02-04 23:49

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_delete_extendeduserexample'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='mobile_num',
            field=phonenumber_field.modelfields.PhoneNumberField(default='0905168988', max_length=128, region=None, unique=True),
            preserve_default=False,
        ),
    ]