from django.contrib import admin

from django.contrib import admin
from .models import Cliente, Sucursal, Pedido, Pago, Administrador, Categoria, Producto, DetallePedido

admin.site.register(Cliente)
admin.site.register(Sucursal)
admin.site.register(Pedido)
admin.site.register(Pago)
admin.site.register(Administrador)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(DetallePedido)
