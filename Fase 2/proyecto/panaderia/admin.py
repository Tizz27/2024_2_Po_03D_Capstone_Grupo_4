from django.contrib import admin
from .models import Cliente, Sucursal, Pedido, Pago, Administrador, Categoria, Producto, DetallePedido

class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'cargo')  # Campos a mostrar en la lista de administración
    search_fields = ('nombre', 'email')  # Permite buscar por nombre y correo
    ordering = ('nombre',)  # Ordena por nombre

# Registro de modelos
admin.site.register(Administrador, AdministradorAdmin)  # Ya se registra con la clase AdministradorAdmin
admin.site.register(Cliente)
admin.site.register(Sucursal)
admin.site.register(Pedido)
admin.site.register(Pago)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(DetallePedido)
