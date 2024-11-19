from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Producto, Cliente,DetallePedido, Pedido, Sucursal
from .forms import ProductoForm,ClienteForm,LoginForm, PedidoForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.contrib import messages
from django.db import transaction
from decimal import Decimal, InvalidOperation
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest



def guardar_pedido(request):
    # Obtener el carrito de la sesión
    carrito = request.session.get('carrito', {})
    sucursales = Sucursal.objects.all()  # Obtener todas las sucursales

    if not carrito:
        messages.error(request, "El carrito está vacío. No se puede proceder con el pedido.")
        return redirect('ver_carrito')

    cliente = None
    if 'cliente_id' in request.session:
        cliente = Cliente.objects.filter(id_cliente=request.session['cliente_id']).first()

    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)

        if pedido_form.is_valid():
            # Crear el pedido sin guardarlo
            pedido = pedido_form.save(commit=False)
            pedido.cliente = cliente

            # Verificar dirección o sucursal
            direccion_envio = request.POST.get('direccion_envio')
            sucursal_id = request.POST.get('sucursal')

            if not direccion_envio and not sucursal_id:
                messages.error(request, "Debes proporcionar una dirección de envío o seleccionar una sucursal.")
                return redirect('ver_carrito')

            # Asignar sucursal si fue seleccionada
            if sucursal_id:
                pedido.sucursal = Sucursal.objects.get(id_sucursal=sucursal_id)

            # Calcular y asignar el total del pedido
            total = request.POST.get('total')
            pedido.total = total
            pedido.save()

            # Crear detalles del pedido
            for key, item in carrito.items():
                producto = Producto.objects.get(pk=key)
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio'],
                    subtotal=item['subtotal']
                )

            # Limpiar el carrito
            request.session['carrito'] = {}
            messages.success(request, "¡Pedido realizado con éxito!")
            return redirect('mostrar_productos')
        else:
            messages.error(request, "Error al guardar el pedido. Verifica la información.")
    else:
        pedido_form = PedidoForm()

    return render(request, 'carrito.html', {
        'carrito': carrito,
        'total': sum(float(item['subtotal']) for item in carrito.values()),
        'pedido_form': pedido_form,
        'sucursales': sucursales,
        'cliente': cliente,
    })


def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(float(item['subtotal']) for item in carrito.values())

    # Verificar si el cliente está autenticado
    cliente_id = request.session.get('cliente_id')
    cliente = None

    if cliente_id:
        try:
            cliente = Cliente.objects.get(id_cliente=cliente_id)
        except Cliente.DoesNotExist:
            messages.error(request, "El cliente no existe. Por favor, regístrate o inicia sesión.")
            return redirect('login1')
    else:
        messages.error(request, "Debes iniciar sesión para realizar un pedido.")
        return redirect('login1')

    # Obtener las sucursales
    sucursales = Sucursal.objects.all()

    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)

        if pedido_form.is_valid():
            # Crear y guardar el pedido
            pedido = pedido_form.save(commit=False)
            pedido.cliente = cliente
            pedido.total = total

            # Asignar sucursal si está seleccionada
            sucursal_id = request.POST.get('sucursal')
            if sucursal_id:
                try:
                    sucursal = Sucursal.objects.get(id_sucursal=sucursal_id)
                    pedido.sucursal = sucursal
                except Sucursal.DoesNotExist:
                    messages.error(request, "La sucursal seleccionada no existe.")
                    return redirect('carrito')

            pedido.save()

            # Guardar los detalles del pedido
            for item in carrito.values():
                producto = Producto.objects.get(id_producto=item['id_producto'])
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item['cantidad'],
                    precio_unitario=item['precio'],
                    subtotal=item['subtotal']
                )

            # Limpiar el carrito y redirigir
            request.session['carrito'] = {}
            messages.success(request, "Pedido realizado con éxito.")
            return redirect('confirmar_pedido')

    else:
        initial_data = {
            'direccion_envio': cliente.direccion if cliente else '',
            'email': cliente.email if cliente else '',
        }
        pedido_form = PedidoForm(initial=initial_data)

    return render(request, 'carrito.html', {
        'carrito': carrito,
        'total': total,
        'pedido_form': pedido_form,
        'sucursales': sucursales,
        'cliente': cliente,  # Pasar el cliente al template
    })


# Modificar la función guardar_carrito_bd para manejar un cliente temporal o una sesión
@transaction.atomic
def guardar_carrito_bd(cliente, carrito):
    if isinstance(cliente, str):  # Si es un ID de sesión
        cliente = Session.objects.get(session_key=cliente)  # Obtén el objeto de sesión correspondiente
        # Aquí puedes almacenar los detalles del pedido asociados con la sesión
        
    # Guardamos el carrito en la base de datos
    for id_producto, item in carrito.items():
        producto = get_object_or_404(Producto, id_producto=id_producto)
        detalle, created = DetallePedido.objects.update_or_create(
            pedido__cliente=cliente,  # Vinculamos al cliente (o sesión)
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

            try:
                cliente = Cliente.objects.get(email=email)

                if cliente.contraseña == contraseña:
                    # Si la contraseña es correcta, guardamos el 'id_cliente' en la sesión
                    request.session['cliente_id'] = cliente.id_cliente

                    # Redirigir al usuario a la página de productos u otra página
                    return redirect('mostrar_productos') 

                else:
                    messages.error(request, 'Correo electrónico o contraseña incorrectos.')
            except Cliente.DoesNotExist:
                messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'login1.html', {'form': form})

def base(request):
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
    return render(request, 'base.html', {'cliente': cliente, 'is_logged_in': bool(cliente)})

def contacto(request):
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
    return render(request, 'contacto.html', {'cliente': cliente, 'is_logged_in': bool(cliente)})


def salir(request):
    logout(request)
    return render (request,'base.html')

def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado exitosamente.')
            return redirect('login1')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
            
    else:
        form = ClienteForm()

    return render(request, 'registrar_cliente.html', {'form': form})



def gestion(request):
    # Obtener el término de búsqueda
    query = request.GET.get('q', '')
    
    # Filtrar los productos si hay un término de búsqueda
    if query:
        productos = Producto.objects.filter(nombre_producto__icontains=query)
    else:
        productos = Producto.objects.all()
    
    # Contar los productos registrados
    productos_count = Producto.objects.count()

    # Contar los clientes registrados
    clientes_count = Cliente.objects.count()

    return render(request, 'gestionproducto.html', {
        'productos': productos,
        'productos_count': productos_count,  # Pasamos el conteo de productos
        'clientes_count': clientes_count
    })

def home(request):
    return render (request,'home.html')

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
            # Redondear el precio a 0 decimales antes de guardar
            precio = form.cleaned_data['precio']
            form.instance.precio = round(precio, 0)
            form.save()
            return redirect('/gestionproducto/')  # Redirige a la lista de productos o a otra página
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'modificar.html', {'form': form, 'producto': producto})

    
def eliminar (request,id_producto):
    productos= get_object_or_404(Producto, id_producto=id_producto)
    productos.delete()
    return redirect(to="/gestionproducto/")   

def mostrar_productos(request):
    query = request.GET.get('q', '')  # Capturar el término de búsqueda
    productos = Producto.objects.filter(nombre_producto__icontains=query) if query else Producto.objects.all()
    cliente_id = request.session.get('cliente_id')
    cliente = None
    if cliente_id:
        try:
            # Obtenemos el cliente desde la base de datos
            cliente = Cliente.objects.get(id_cliente=cliente_id)
        except Cliente.DoesNotExist:
            return redirect('login1')  # Si el cliente no existe, redirigir al login
    # Pasar los productos y cliente al template
    return render(request, 'mostrar_productos.html', {'productos': productos, 'query': query, 'cliente': cliente, 'is_logged_in': bool(cliente)})

def cerrar(request):
    logout(request)
    return render (request,'base.html')

