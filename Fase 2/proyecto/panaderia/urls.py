from django.urls import path
from .views import menu, modificar,eliminar,registrar_producto,base, mostrar_productos,registrar_cliente, login,agregar_al_carrito,ver_carrito,eliminar_del_carrito,confirmar_pedido

urlpatterns =[
    path('menu/', menu, name='menu'),
    path('modificar/<id_producto>/', modificar, name='modificar'),
    path('eliminar/<id_producto>/', eliminar, name='eliminar'),
    path('registrar/', registrar_producto, name='registrar_producto'),
    path('base/', base, name='base'),
    path('productos/',mostrar_productos, name='mostrar_productos'),
    path('registrocliente/',registrar_cliente, name='registrar_cliente'),
    path('login/',login, name='login'),
    path('agregar_al_carrito/<int:producto_id>/',agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', ver_carrito, name='ver_carrito'),
    path('eliminar_del_carrito/<int:producto_id>/',eliminar_del_carrito, name='eliminar_del_carrito'),
    path('confirmar_pedido/', confirmar_pedido, name='confirmar_pedido'),
]

