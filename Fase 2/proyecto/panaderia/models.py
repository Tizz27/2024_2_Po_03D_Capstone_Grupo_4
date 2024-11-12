from django.db import models

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)  # AutoField crea un ID auto-incremental
    nombre_completo = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    rut = models.CharField(max_length=12, unique=True)
    fecha_registro = models.DateField(auto_now_add=True)  # Se registra automáticamente la fecha

    class Meta:
        db_table = 'Cliente'

class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=30)

    class Meta:
        db_table = 'Sucursales'

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField()
    estado = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=7, decimal_places=2)
    direccion_envio = models.CharField(max_length=255, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='pedidos')

    class Meta:
        db_table = 'Pedido'

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=7, decimal_places=2)
    metodo_pago = models.CharField(max_length=50)
    estado = models.CharField(max_length=20)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='pagos')

    class Meta:
        db_table = 'Pago'

class Administrador(models.Model):
    id_adm = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    cargo = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Administrador'

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)  # CLOB se mapea a TextField en Django
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name='categorias')

    class Meta:
        db_table = 'Categoria'

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to="img/productos/")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name='productos')

    class Meta:
        db_table = 'Producto'

class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=7, decimal_places=2)
    subtotal = models.DecimalField(max_digits=7, decimal_places=2)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles')

    class Meta:
        db_table = 'Detalle_Pedido'
