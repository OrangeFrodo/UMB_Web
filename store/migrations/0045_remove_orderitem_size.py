# Generated by Django 3.1.3 on 2021-02-08 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0044_auto_20210208_0344'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='size',
        ),
    ]