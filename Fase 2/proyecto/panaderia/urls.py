from django.urls import path
from .views import menu, modificar,eliminar,registrar_producto,base, mostrar_productos,registrar_cliente

urlpatterns =[
    path('menu/', menu, name='menu'),
    path('modificar/<id_producto>/', modificar, name='modificar'),
    path('eliminar/<id_producto>/', eliminar, name='eliminar'),
    path('registrar/', registrar_producto, name='registrar_producto'),
    path('base/', base, name='base'),
    path('productos/',mostrar_productos, name='mostrar_productos'),
    path('login/',registrar_cliente, name='registrar_cliente'),

]