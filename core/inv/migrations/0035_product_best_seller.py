# Generated by Django 4.0.5 on 2022-11-19 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0034_product_featured_products_product_is_hot_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='best_seller',
            field=models.BooleanField(default=False, verbose_name='Más vendidos'),
        ),
    ]
