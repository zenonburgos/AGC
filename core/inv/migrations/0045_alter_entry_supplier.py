# Generated by Django 4.0.5 on 2022-12-04 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0044_alter_entry_nulled_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inv.supplier'),
        ),
    ]
