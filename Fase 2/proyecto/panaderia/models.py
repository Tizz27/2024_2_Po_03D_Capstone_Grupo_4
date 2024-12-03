from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)  # AutoField crea un ID auto-incremental
    nombre_completo = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    rut = models.CharField(max_length=9, unique=True)
    fecha_registro = models.DateField(auto_now_add=True)  # Se registra automáticamente la fecha
    def __str__(self):
        return self.email

    class Meta:
        db_table = 'Cliente'

class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=50)
    ciudad = models.CharField(max_length=30)
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Sucursal'

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateField(default=timezone.now) 
    estado = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=7, decimal_places=0)
    direccion_envio = models.CharField(max_length=255, blank=True, null=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='pedidos', null=True, blank=True)
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.estado
    class Meta:
        db_table = 'Pedido'

class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    fecha_pago = models.DateField()
    monto = models.DecimalField(max_digits=7, decimal_places=0)
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
    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Administrador'

class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)  # CLOB se mapea a TextField en Django
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name='categorias')
    def __str__(self):
        return self.nombre_categoria 

    class Meta:
        db_table = 'Categoria'

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100)
    precio_adicional = models.DecimalField(max_digits=5, decimal_places=0)

    def __str__(self):
        return self.nombre
    
class Tamaño(models.Model):
    nombre = models.CharField(max_length=50)  # Ejemplo: "Pequeño", "Mediano", "Grande"
    precio_adicional = models.DecimalField(max_digits=6, decimal_places=0)  # Precio adicional por el tamaño

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'Tamaño'

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    precio = models.DecimalField(max_digits=6, decimal_places=0)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to="img/productos/")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name='productos')
    ingredientes = models.ManyToManyField(Ingrediente, related_name='productos', blank=True)  # Relación con Ingredientes
    tamaño = models.ManyToManyField(Tamaño, related_name='productos', blank=True)
    cantidad_minima = models.IntegerField(default=1,null=True, blank=True)  # Cantidad mínima de venta, por ejemplo 1 unidad
    cantidad_maxima = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre_producto

    class Meta:
        db_table = 'Producto'

class DetallePedido(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=7, decimal_places=0)
    subtotal = models.DecimalField(max_digits=7, decimal_places=0)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles')
    tamaño = models.ForeignKey(Tamaño, on_delete=models.CASCADE, related_name='detalles', null=True, blank=True)  # Nuevo campo
    ingredientes = models.ManyToManyField(Ingrediente, related_name='detalles', blank=True)  # Nuevo campo
    
    class Meta:
        db_table = 'Detalle_Pedido'

        


