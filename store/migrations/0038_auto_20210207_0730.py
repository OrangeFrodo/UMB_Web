# Generated by Django 3.1.3 on 2021-02-07 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0037_auto_20210206_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='krstné_meno'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='priezvisko'),
        ),
    ]
