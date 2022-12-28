# Generated by Django 4.0.5 on 2022-10-21 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0021_product_marca_product_proper_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='proper_name',
            new_name='root_name',
        ),
        migrations.AddField(
            model_name='product',
            name='catalogue',
            field=models.BooleanField(default=True, verbose_name='Aparece en catálogo'),
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.BooleanField(default=True, verbose_name='Aparece en la web'),
        ),
    ]
