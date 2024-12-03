# Generated by Django 5.1.2 on 2024-12-02 20:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panaderia', '0005_detallepedido_ingredientes_adicionales_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallepedido',
            name='ingredientes_adicionales',
            field=models.ManyToManyField(blank=True, related_name='detalles', to='panaderia.ingrediente'),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='tamaño',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='panaderia.tamaño'),
        ),
    ]
