from django.urls import path
from .views import base,menu, modificar,eliminar,registrar_producto,base, mostrar_productos,registrar_cliente, salir

urlpatterns =[
    path('', base, name='base'),
    path('menu/', menu, name='menu'),
    path('modificar/<id_producto>/', modificar, name='modificar'),
    path('eliminar/<id_producto>/', eliminar, name='eliminar'),
    path('registrar/', registrar_producto, name='registrar_producto'),
    path('productos/',mostrar_productos, name='mostrar_productos'),
    path('registrocliente/',registrar_cliente, name='registrar_cliente'),
    path('salir/', salir, name='salir'),
    
   
]
