# Generated by Django 3.2.7 on 2021-10-05 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20211005_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, default='images/cute.jfif', null=True, upload_to='images/product_images/'),
        ),
    ]
