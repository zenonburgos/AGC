# Generated by Django 4.0.5 on 2022-10-29 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0028_remove_supplier_date_of_birth_remove_supplier_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.BooleanField(default=False, verbose_name='Aparece en la web store'),
        ),
    ]
