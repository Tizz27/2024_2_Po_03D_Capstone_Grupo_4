from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Producto, Cliente,DetallePedido
from .forms import ProductoForm
from .forms import ClienteForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from .forms import LoginForm
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import transaction
from decimal import Decimal, InvalidOperation

def ver_carrito(request):
    carrito = {}
    total = Decimal(0)  # Usamos Decimal para evitar problemas de precisión

    # Si el cliente está autenticado, carga el carrito desde la base de datos
    if request.user.is_authenticated:
        carrito_items = DetallePedido.objects.filter(pedido__cliente=request.user)
        carrito = {
            item.producto.id_producto: {
                'nombre': item.producto.nombre_producto,
                'precio': str(item.precio_unitario),  # Convertimos a string solo al mostrar
                'cantidad': item.cantidad,
                'subtotal': str(item.subtotal)  # Convertimos a string solo al mostrar
            }
            for item in carrito_items
        }
        
        # Sumar el total con manejo de errores
        for item in carrito.values():
            try:
                total += Decimal(item['subtotal'])
            except InvalidOperation:
                # Si hay un error de conversión, se ignora ese valor
                continue
    else:
        # Si no está autenticado, utiliza el carrito de la sesión
        carrito = request.session.get('carrito', {})
        for item in carrito.values():
            try:
                total += Decimal(item['subtotal'])
            except InvalidOperation:
                # Si hay un error de conversión, se ignora ese valor
                continue

    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})

@transaction.atomic
def guardar_carrito_bd(cliente, carrito):
    # Guardamos el carrito en la base de datos
    for id_producto, item in carrito.items():
        producto = get_object_or_404(Producto, id_producto=id_producto)
        detalle, created = DetallePedido.objects.update_or_create(
            pedido__cliente=cliente,  # Vinculamos al cliente
            producto=producto,
            defaults={
                'cantidad': item['cantidad'],
                'precio_unitario': item['precio'],
                'subtotal': item['subtotal']
            }
        )

# Luego, la vista agregar_al_carrito puede llamar a esta función
def agregar_al_carrito(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    cliente = request.user if request.user.is_authenticated else None

    # Verificar si el carrito ya está en la sesión
    if 'carrito' not in request.session:
        request.session['carrito'] = {}

    carrito = request.session['carrito']

    # Si el producto ya está en el carrito, aumentamos la cantidad
    if str(id_producto) in carrito:
        carrito[str(id_producto)]['cantidad'] += 1
        carrito[str(id_producto)]['subtotal'] = str(float(carrito[str(id_producto)]['precio']) * carrito[str(id_producto)]['cantidad'])
    else:
        # Agregar el producto al carrito con cantidad inicial de 1
        carrito[str(id_producto)] = {
            'nombre': producto.nombre_producto,
            'precio': str(producto.precio),
            'cantidad': 1,
            'subtotal': str(producto.precio)
        }

    # Guardar el carrito actualizado en la sesión
    request.session['carrito'] = carrito

    # Si el cliente está autenticado, transferimos el carrito de la sesión a la base de datos
    if cliente:
        guardar_carrito_bd(cliente, carrito)

    messages.success(request, f"Se ha agregado {producto.nombre_producto} al carrito.")
    return redirect('mostrar_productos')



def eliminar_del_carrito(request, id_producto):
    cliente = request.user if request.user.is_authenticated else None

    # Eliminar el producto del carrito de la sesión
    carrito = request.session.get('carrito', {})
    if str(id_producto) in carrito:
        if carrito[str(id_producto)]['cantidad'] > 1:
            carrito[str(id_producto)]['cantidad'] -= 1
            carrito[str(id_producto)]['subtotal'] = str(float(carrito[str(id_producto)]['precio']) * carrito[str(id_producto)]['cantidad'])
        else:
            del carrito[str(id_producto)]
        request.session['carrito'] = carrito

    # Eliminar de la base de datos si el cliente está autenticado
    if cliente:
        producto = get_object_or_404(Producto, id_producto=id_producto)
        DetallePedido.objects.filter(pedido__cliente=cliente, producto=producto).delete()

    return redirect('ver_carrito')

def login_view(request): 
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contraseña']
            
            # Intentar encontrar el cliente por su email
            try:
                cliente = Cliente.objects.get(email=email)
                
                # Verificar que la contraseña coincida
                if cliente.contraseña == contraseña:
                    # Si la contraseña es correcta, guardamos el 'id_cliente' en la sesión
                    request.session['cliente_id'] = cliente.id_cliente

                    # Sincronizar el carrito de la sesión con la base de datos
                    if 'carrito' in request.session:
                        carrito = request.session['carrito']
                        guardar_carrito_bd(cliente, carrito)
                        # Limpiar el carrito de la sesión
                        del request.session['carrito']

                    # Redirigir al usuario a la página de productos u otra página
                    return redirect('mostrar_productos') 

                else:
                    messages.error(request, 'Correo electrónico o contraseña incorrectos.')
            except Cliente.DoesNotExist:
                messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'login1.html', {'form': form})

def home(request):
    # Verificamos si el cliente está logueado
    cliente_id = request.session.get('cliente_id')
    cliente = None
    if cliente_id:
        try:
            # Obtenemos el cliente desde la base de datos
            cliente = Cliente.objects.get(id_cliente=cliente_id)
        except Cliente.DoesNotExist:
            return redirect('login1')  # Si el cliente no existe, redirigir al login

    # Pasamos el cliente y el estado de la sesión al template
    return render(request, 'home.html', {'cliente': cliente, 'is_logged_in': bool(cliente)})

def cerrar_sesion(request):
    if 'cliente_id' in request.session:
        del request.session['cliente_id']
    return redirect('home.html')


def salir(request):
    logout(request)
    return render (request,'base.html')

def registrar_cliente(request):
    data = {'form': ClienteForm()}

    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST, files=request.FILES)

        # Validar RUT
        rut = request.POST.get('rut')
        if not validar_rut(rut):
            data["mensaje"] = "RUT inválido"
            return render(request, 'registrar_cliente.html', data)

        if formulario.is_valid():
            cliente = formulario.save(commit=False)
            cliente.contraseña = make_password(cliente.contraseña)
            cliente.save()
            data["mensaje"] = "Cliente registrado"
            return redirect('base.html')

    return render(request, 'registrar_cliente.html', data)



def gestion(request):
    listaproductos= Producto.objects.all()
    return render(request,"gestionproducto.html", {"productos": listaproductos})

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
    return redirect(to="gestionproducto")   

def mostrar_productos(request):
    productos = Producto.objects.all()
    cliente_id = request.session.get('cliente_id')
    cliente = None
    if cliente_id:
        try:
            # Obtenemos el cliente desde la base de datos
            cliente = Cliente.objects.get(id_cliente=cliente_id)
        except Cliente.DoesNotExist:
            return redirect('login1')  # Si el cliente no existe, redirigir al login
    # Pasar los productos y cliente al template
    return render(request, 'mostrar_productos.html', {'productos': productos, 'cliente': cliente, 'is_logged_in': bool(cliente)})





def base(request):
    return render(request, 'base.html')


def cerrar(request):
    logout(request)
    return render (request,'home.html')