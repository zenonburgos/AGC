# Generated by Django 4.0.5 on 2022-10-19 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0017_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Nombre'),
        ),
    ]
