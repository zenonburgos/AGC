# Generated by Django 4.0.5 on 2022-11-02 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0032_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='group',
        ),
    ]
