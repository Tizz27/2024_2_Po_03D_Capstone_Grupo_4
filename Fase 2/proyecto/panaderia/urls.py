from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.menu, name='menu'),
    path('menu/', views.menu, name='menu'),
    path('productos/', views.productos, name='productos'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('modificar/<id>/', views.modificar, name='modificar'),
    path('eliminar/<id>/', views.eliminar, name='eliminar'),
    path('lista_productos/', views.lista_productos, name='lista_productos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)