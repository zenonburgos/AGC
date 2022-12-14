# Generated by Django 4.0.5 on 2022-12-02 00:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0039_alter_product_brand_alter_product_fact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='nulled',
            field=models.BooleanField(default=False, verbose_name='Anulado'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inv.brand', verbose_name='Marca'),
        ),
    ]
