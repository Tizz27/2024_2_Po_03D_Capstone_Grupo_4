# Generated by Django 5.1.2 on 2024-10-30 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panaderia', '0002_alter_producto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(upload_to='img/productos/'),
        ),
    ]
