# Generated by Django 3.2.7 on 2022-09-03 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inv', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category/%Y/%m/%d', verbose_name='Imagen'),
        ),
    ]
