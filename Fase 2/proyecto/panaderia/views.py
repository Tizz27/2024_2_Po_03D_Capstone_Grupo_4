from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Producto
from .forms import ProductoForm
from .forms import ClienteForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm



# views.py
from .models import DetallePedido, Pedido, Producto
from django.contrib.sessions.models import Session
from django.db import transaction
from django.http import JsonResponse

from django.http import JsonResponse
from .models import Producto  # Asegúrate de importar el modelo correcto

def agregar_al_carrito(request, producto_id):
    # Suponiendo que `Carrito` es un diccionario que contiene los productos en el carrito
    carrito = request.session.get('carrito', {})

    # Lógica para agregar un producto
    producto = Producto.objects.get(id=producto_id)
    if producto_id in carrito:
        carrito[producto_id]['cantidad'] += 1
    else:
        carrito[producto_id] = {
            'nombre': producto.nombre_producto,
            'precio': producto.precio,
            'cantidad': 1
        }
    
    # Guarda el carrito actualizado en la sesión
    request.session['carrito'] = carrito

    # Crea `carrito_data` basado en el carrito
    carrito_data = [{'id': pid, 'nombre': p['nombre'], 'precio': p['precio'], 'cantidad': p['cantidad']} for pid, p in carrito.items()]
    total = sum(p['precio'] * p['cantidad'] for p in carrito.values())
    carrito_data.append({'total': total})  # Agrega el total

    return JsonResponse({'mensaje': 'Producto agregado al carrito', 'carrito': carrito_data})

def eliminar_del_carrito(request, producto_id):
    # Obtener el carrito de la sesión
    carrito = request.session.get('carrito', {})

    # Lógica para eliminar un producto
    if producto_id in carrito:
        del carrito[producto_id]
        request.session['carrito'] = carrito  # Actualiza la sesión

    # Crea `carrito_data` con el carrito actualizado
    carrito_data = [{'id': pid, 'nombre': p['nombre'], 'precio': p['precio'], 'cantidad': p['cantidad']} for pid, p in carrito.items()]
    total = sum(p['precio'] * p['cantidad'] for p in carrito.values())
    carrito_data.append({'total': total})

    return JsonResponse({'mensaje': 'Producto eliminado del carrito', 'carrito': carrito_data})


def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['cantidad'] * item['precio'] for item in carrito.values())
    return render(request, 'mostrar_productos.html', {'carrito': carrito, 'total': total})



@transaction.atomic
def confirmar_pedido(request):
    cliente = request.user.cliente  # Suponiendo que el cliente está autenticado
    carrito = request.session.get('carrito', {})

    if not carrito:
        return redirect('ver_carrito')

    # Crear un nuevo pedido
    pedido = Pedido.objects.create(
        cliente=cliente,
        fecha_pedido=date.today(),
        estado='Pendiente',
        total=sum(item['cantidad'] * item['precio'] for item in carrito.values()),
        direccion_envio='Dirección del cliente',
        sucursal_id=1  # Suponiendo una sucursal por defecto
    )

    # Guardar los detalles del pedido
    for producto_id, item in carrito.items():
        producto = Producto.objects.get(id_producto=producto_id)
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item['cantidad'],
            precio_unitario=item['precio'],
            subtotal=item['cantidad'] * item['precio']
        )

    # Limpiar el carrito de la sesión
    request.session['carrito'] = {}
    return redirect('confirmacion')

def registrar_cliente(request):
    data = {'form': ClienteForm()}

    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST, files=request.FILES)

        # Validar RUT
        rut = request.POST.get('rut')
        if not validar_rut(rut):
            data["mensaje"] = "RUT inválido"
            return render(request, 'login_cliente.html', data)

        if formulario.is_valid():
            cliente = formulario.save(commit=False)
            cliente.contraseña = make_password(cliente.contraseña)
            cliente.save()
            data["mensaje"] = "Cliente registrado"
            return redirect('menu')

    return render(request, 'login_cliente.html', data)


def validar_rut(rut):
    # Separar el número y el dígito verificador
    rut = rut.replace(".", "").replace("-", "")
    if len(rut) < 2:
        return False
    
    numero = rut[:-1]
    dv = rut[-1].upper()

    # Calcular el dígito verificador
    suma = 0
    multiplo = 2

    for i in reversed(range(len(numero))):
        suma += int(numero[i]) * multiplo
        multiplo = 9 if multiplo == 7 else multiplo + 1

    dv_calculado = 11 - (suma % 11)

    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'

    return str(dv_calculado) == dv


def menu(request):
    listaproductos= Producto.objects.all()
    return render(request,"menu.html", {"productos": listaproductos})

def base(request):
    return render (request,'base.html')

def registrar_producto(request):
    data = {
         'form': ProductoForm()}         
    if request.method == 'POST':
        formulario = ProductoForm(data= request.POST, files= request.FILES)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"]= "Producto registrado",                                                
    return render(request, 'registrar_producto.html', data)

def modificar(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('mostrar_productos')  # Redirige a la lista de productos o a otra página
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'modificar.html', {'form': form, 'producto': producto})  

    
def eliminar (request,id_producto):
    productos= get_object_or_404(Producto, id_producto=id_producto)
    productos.delete()
    return redirect(to="menu")   

def mostrar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'mostrar_productos.html', {'productos': productos})

def login_cliente(request):
    # Si el usuario ya está logueado, redirigir
    if request.user.is_authenticated:
        return redirect('menu')  # Redirige si ya está logueado
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Intentar autenticar al usuario
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Si la autenticación fue exitosa, iniciar sesión
                login(request, user)
                return redirect('menu')  # Redirige al menú
            else:
                # Si las credenciales son incorrectas
                messages.error(request, 'Credenciales incorrectas, intente nuevamente.')

    else:
        form = AuthenticationForm()

    # Renderizar el formulario
    return render(request, 'login.html', {'form': form})

def base(request):
    return render(request, 'base.html')