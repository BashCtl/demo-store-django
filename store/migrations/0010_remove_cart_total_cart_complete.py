# Generated by Django 4.2.7 on 2023-12-05 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_remove_cart_user_alter_cartitem_product_cart_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='total',
        ),
        migrations.AddField(
            model_name='cart',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
