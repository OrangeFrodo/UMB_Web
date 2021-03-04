# Generated by Django 3.1.3 on 2021-02-08 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0042_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(blank=True, choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], default='M', max_length=4, null=True),
        ),
    ]
