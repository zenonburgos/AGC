# Generated by Django 4.0.5 on 2023-01-25 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0057_alter_entry_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='doc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inv.tiposdoc'),
        ),
    ]
