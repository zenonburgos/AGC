# Generated by Django 4.0.5 on 2023-01-27 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0060_rename_type_tiposdoc_movtype'),
    ]

    operations = [
        migrations.AddField(
            model_name='movements',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inv.branch'),
            preserve_default=False,
        ),
    ]
