# Generated by Django 5.1.2 on 2024-12-01 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panaderia', '0003_tamaño_producto_tamaño'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='cantidad_maxima',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='cantidad_minima',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
