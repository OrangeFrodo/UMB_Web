# Generated by Django 3.1.3 on 2021-02-04 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0028_auto_20210205_0043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='phone',
        ),
    ]
