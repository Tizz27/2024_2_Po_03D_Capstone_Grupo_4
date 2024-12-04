from django.urls import path,include
from .views import gestion, modificar,procesar_pago,pago_exitoso,pago_cancelado,listar_clientes,productos,pedidos,registrar_administrador,eliminar_cliente,eliminar,registrar_producto,base,guardar_pedido, mostrar_productos,registrar_cliente, salir, login_view,home,cerrar,agregar_al_carrito,ver_carrito,eliminar_del_carrito,contacto

urlpatterns =[
    path('', base, name='base'),
    path('gestionproducto/', gestion, name='gestion'),
    path('modificar/<id_producto>/', modificar, name='modificar'),
    path('eliminar/<id_producto>/', eliminar, name='eliminar'),
    path('registrar/', registrar_producto, name='registrar_producto'),
    path('productos/',mostrar_productos, name='mostrar_productos'),
    path('registro/', registrar_cliente, name='registrar_cliente'),
    path('salir/', salir, name='salir'),
    path('login1/', login_view, name='login1'),
    path('home/', home, name='home'),
    path('contacto/', contacto, name='contacto'),
    path('cerrar/',cerrar, name='cerrar'), 
    path('agregar_al_carrito/<int:id_producto>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/',ver_carrito, name='ver_carrito'),
    path('eliminar_del_carrito/<str:id_producto>/',eliminar_del_carrito, name='eliminar_del_carrito'),
    path('guardar_pedido/', guardar_pedido, name='guardar_pedido'),
    path('clientes/', listar_clientes, name='listar_clientes'),
    path('eliminar_cliente/<int:id_cliente>/', eliminar_cliente, name='eliminar_cliente'),
    path('registroadmin/',registrar_administrador, name='registroadmin'), 
    path('pedidos/', pedidos, name='pedidos'),
    path('productos/<str:categoria>/', productos, name='productos_categoria'),
    path('nuevo/', productos, name='productos_todos'),
    path('pago_exitoso/', pago_exitoso, name='pago_exitoso'),
    path('pago_cancelado/', pago_cancelado, name='pago_cancelado'),
    path('procesar_pago/', procesar_pago, name='procesar_pago'),
	
    
    
    
    
]

    
