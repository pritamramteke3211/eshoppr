# Generated by Django 3.2.7 on 2021-10-09 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_remove_order_delivery_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='Name',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='address',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
        migrations.AddField(
            model_name='ordered_address',
            name='Name',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='ordered_address',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254),
        ),
    ]