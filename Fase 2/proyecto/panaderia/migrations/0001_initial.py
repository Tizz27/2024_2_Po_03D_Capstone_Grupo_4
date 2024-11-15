# Generated by Django 5.1.2 on 2024-10-29 20:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id_adm', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contraseña', models.CharField(max_length=255)),
                ('cargo', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'Administrador',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_completo', models.CharField(max_length=50)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('contraseña', models.CharField(max_length=255)),
                ('direccion', models.CharField(blank=True, max_length=200, null=True)),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('fecha_registro', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Cliente',
            },
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id_sucursal', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('direccion', models.CharField(max_length=50)),
                ('ciudad', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'Sucursales',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_categoria', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categorias', to='panaderia.administrador')),
            ],
            options={
                'db_table': 'Categoria',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id_pedido', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_pedido', models.DateField()),
                ('estado', models.CharField(max_length=20)),
                ('total', models.DecimalField(decimal_places=2, max_digits=7)),
                ('direccion_envio', models.CharField(blank=True, max_length=255, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='panaderia.cliente')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='panaderia.sucursal')),
            ],
            options={
                'db_table': 'Pedido',
            },
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id_pago', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_pago', models.DateField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=7)),
                ('metodo_pago', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=20)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos', to='panaderia.pedido')),
            ],
            options={
                'db_table': 'Pago',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_producto', models.CharField(max_length=30)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('stock', models.IntegerField()),
                ('imagen', models.BinaryField(blank=True, null=True)),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='panaderia.administrador')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='panaderia.categoria')),
            ],
            options={
                'db_table': 'Producto',
            },
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id_detalle', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('precio_unitario', models.DecimalField(decimal_places=2, max_digits=7)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=7)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='panaderia.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='panaderia.producto')),
            ],
            options={
                'db_table': 'Detalle_Pedido',
            },
        ),
    ]
