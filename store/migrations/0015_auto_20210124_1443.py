# Generated by Django 3.1.5 on 2021-01-24 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_coupon_ammount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='ammount',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
