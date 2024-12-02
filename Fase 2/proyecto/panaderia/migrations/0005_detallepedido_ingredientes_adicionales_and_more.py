# Generated by Django 5.1.2 on 2024-12-01 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panaderia', '0004_producto_cantidad_maxima_producto_cantidad_minima'),
    ]

    operations = [
        migrations.AddField(
            model_name='detallepedido',
            name='ingredientes_adicionales',
            field=models.ManyToManyField(blank=True, to='panaderia.ingrediente'),
        ),
        migrations.AddField(
            model_name='detallepedido',
            name='tamaño',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='panaderia.tamaño'),
        ),
    ]
