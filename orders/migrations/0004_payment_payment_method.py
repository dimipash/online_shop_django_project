# Generated by Django 5.0.3 on 2024-03-28 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_payment_order_payment_orderproduct_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(default=11, max_length=100),
            preserve_default=False,
        ),
    ]
