from django.urls import path
from .views import base,gestion, modificar,eliminar,registrar_producto,base, mostrar_productos,registrar_cliente, salir, login_view,home,cerrar

urlpatterns =[
    path('', base, name='base'),
    path('gestionproducto/', gestion, name='gestion'),
    path('modificar/<id_producto>/', modificar, name='modificar'),
    path('eliminar/<id_producto>/', eliminar, name='eliminar'),
    path('registrar/', registrar_producto, name='registrar_producto'),
    path('productos/',mostrar_productos, name='mostrar_productos'),
    path('registrocliente/',registrar_cliente, name='registrar_cliente'),
    path('salir/', salir, name='salir'),
    path('login1/', login_view, name='login1'),
    path('home/', home, name='home'),
    path('cerrar/',cerrar, name='cerrar'), 

    
   
]
