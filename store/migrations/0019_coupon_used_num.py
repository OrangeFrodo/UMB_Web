# Generated by Django 3.1.3 on 2021-02-01 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_order_temporary_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='used_num',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
