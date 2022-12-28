# Generated by Django 4.0.5 on 2022-11-29 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0038_alter_tiposdoc_last_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inv.brand', verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='product',
            name='fact',
            field=models.FloatField(blank=True, default=0.58, null=True, verbose_name='Factor'),
        ),
        migrations.AlterField(
            model_name='product',
            name='fact2',
            field=models.FloatField(blank=True, default=0.65, null=True, verbose_name='Factor 2'),
        ),
        migrations.AlterField(
            model_name='product',
            name='fact3',
            field=models.FloatField(blank=True, default=0.7, null=True, verbose_name='Factor 3'),
        ),
    ]
