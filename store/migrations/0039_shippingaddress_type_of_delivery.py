# Generated by Django 3.1.3 on 2021-02-07 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0038_auto_20210207_0730'),
    ]

    operations = [
        migrations.AddField(
            model_name='shippingaddress',
            name='type_of_delivery',
            field=models.CharField(default='Kurier', max_length=200),
            preserve_default=False,
        ),
    ]
