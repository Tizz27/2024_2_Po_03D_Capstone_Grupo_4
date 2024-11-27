from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Cliente,DetallePedido, Sucursal
from .forms import ProductoForm,ClienteForm,LoginForm, PedidoForm, AdministradorForm,CustomUserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.contrib import messages
from django.db import transaction

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto, Pedido, DetallePedido, Sucursal, Cliente
from django.utils.timezone import now



# Función auxiliar para calcular el total del carrito
def calcular_total_carrito(carrito):
    return sum(float(item['subtotal']) for item in carrito.values())

# Función auxiliar para guardar los detalles del pedido
def guardar_detalles_pedido(pedido, carrito):
    for key, item in carrito.items():
        producto = Producto.objects.get(pk=key)
        DetallePedido.objects.create(
            pedido=pedido,
            producto=producto,
            cantidad=item['cantidad'],
            precio_unitario=producto.precio,  # Validación de precios desde el backend
            subtotal=producto.precio * item['cantidad']  # Cálculo seguro del subtotal
        )

# Vista para ver el carrito
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = calcular_total_carrito(carrito)

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

    sucursales = Sucursal.objects.all()

    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        if pedido_form.is_valid():
            try:
                with transaction.atomic():
                    # Crear el pedido
                    pedido = pedido_form.save(commit=False)
                    pedido.cliente = cliente
                    pedido.total = total

                    # Asignar sucursal si fue seleccionada
                    sucursal_id = request.POST.get('sucursal')
                    if sucursal_id:
                        pedido.sucursal = get_object_or_404(Sucursal, id_sucursal=sucursal_id)

                    pedido.save()

                    # Guardar detalles del pedido
                    guardar_detalles_pedido(pedido, carrito)

                    # Limpiar el carrito
                    request.session['carrito'] = {}
                    messages.success(request, "¡Pedido realizado con éxito!")
                    return redirect('mostrar_productos')
            except Exception as e:
                messages.error(request, f"Hubo un error al guardar el pedido: {str(e)}")
        else:
            messages.error(request, "Por favor verifica la información ingresada.")
    else:
        pedido_form = PedidoForm(initial={
            'direccion_envio': cliente.direccion if cliente else '',
            'email': cliente.email if cliente else '',
        })

    return render(request, 'carrito.html', {
        'carrito': carrito,
        'total': total,
        'pedido_form': pedido_form,
        'sucursales': sucursales,
    })

def guardar_pedido(request):
    # Recuperar el carrito de la sesión
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.error(request, "El carrito está vacío. No se puede proceder con el pedido.")
        return redirect('ver_carrito')

    # Recuperar el cliente de la sesión
    cliente = None
    if 'cliente_id' in request.session:
        cliente = Cliente.objects.filter(id_cliente=request.session['cliente_id']).first()
    if not cliente:
        messages.error(request, "Debes iniciar sesión para realizar un pedido.")
        return redirect('login1')

    if request.method == 'POST':
        tipo_entrega = request.POST.get('tipo_entrega')
        direccion_envio = request.POST.get('direccion_envio') if tipo_entrega == 'envio' else None
        sucursal_id = request.POST.get('sucursal') if tipo_entrega == 'sucursal' else None

        if tipo_entrega == 'envio' and not direccion_envio:
            messages.error(request, "Por favor, proporciona una dirección de envío.")
            return redirect('ver_carrito')
        if tipo_entrega == 'sucursal' and not sucursal_id:
            messages.error(request, "Por favor, selecciona una sucursal.")
            return redirect('ver_carrito')

        try:
            with transaction.atomic():
                # Crear el pedido
                sucursal = Sucursal.objects.get(pk=sucursal_id) if sucursal_id else None
                total = sum(float(item['subtotal']) for item in carrito.values())

                pedido = Pedido.objects.create(
                    cliente=cliente,
                    total=total,
                    direccion_envio=direccion_envio,
                    sucursal=sucursal,
                    fecha_entrega=request.POST.get('fecha_entrega'),
                    comentarios=request.POST.get('comentarios'),
                    estado='Pendiente',  # Cambia según sea necesario
                )

                # Crear los detalles del pedido
                for key, item in carrito.items():
                    producto = get_object_or_404(Producto, pk=key)
                    DetallePedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=item['cantidad'],
                        precio_unitario=float(item['precio']),
                        subtotal=float(item['subtotal']),
                    )

                # Limpiar el carrito
                request.session['carrito'] = {}
                messages.success(request, "¡Pedido realizado con éxito!")
                return redirect('mostrar_productos')

        except Exception as e:
            messages.error(request, f"Hubo un error al guardar el pedido: {str(e)}")

    sucursales = Sucursal.objects.all()
    return render(request, 'carrito.html', {
        'carrito': carrito,
        'total': sum(float(item['subtotal']) for item in carrito.values()),
        'sucursales': sucursales,
        'cliente': cliente,
    })
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(float(item['subtotal']) for item in carrito.values())

    cliente_id = request.session.get('cliente_id')
    cliente = None

    if cliente_id:
        cliente = Cliente.objects.filter(id_cliente=cliente_id).first()
        if not cliente:
            messages.error(request, "El cliente no existe. Por favor, regístrate o inicia sesión.")
            return redirect('login1')
    else:
        messages.error(request, "Debes iniciar sesión para realizar un pedido.")
        return redirect('login1')

    sucursales = Sucursal.objects.all()

    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)

        if pedido_form.is_valid():
            try:
                with transaction.atomic():
                    pedido = pedido_form.save(commit=False)
                    pedido.cliente = cliente
                    pedido.total = total

                    sucursal_id = request.POST.get('sucursal')
                    if sucursal_id:
                        sucursal = get_object_or_404(Sucursal, id_sucursal=sucursal_id)
                        pedido.sucursal = sucursal

                    pedido.save()

                    # Guardar detalles del carrito como objetos DetallePedido
                    for key, item in carrito.items():
                        producto = get_object_or_404(Producto, id_producto=key)
                        DetallePedido.objects.create(
                            pedido=pedido,
                            producto=producto,
                            cantidad=item['cantidad'],
                            precio_unitario=float(item['precio']),
                            subtotal=float(item['subtotal']),
                        )

                    # Limpiar el carrito
                    request.session['carrito'] = {}
                    messages.success(request, "Pedido realizado con éxito.")
                    return redirect('mostrar_productos')

            except Exception as e:
                messages.error(request, f"Error al guardar el pedido: {str(e)}")
        else:
            print(pedido_form.errors)
            messages.error(request, "Error en los datos del formulario. Por favor, verifica los campos.")
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
    })

# Vista para agregar un producto al carrito
def agregar_al_carrito(request, id_producto):
    producto = get_object_or_404(Producto, id_producto=id_producto)
    if 'carrito' not in request.session:
        request.session['carrito'] = {}

    carrito = request.session['carrito']

    # Actualizar cantidad y subtotal si el producto ya está en el carrito
    if str(id_producto) in carrito:
        carrito[str(id_producto)]['cantidad'] += 1
        carrito[str(id_producto)]['subtotal'] = str(
            float(carrito[str(id_producto)]['precio']) * carrito[str(id_producto)]['cantidad']
        )
    else:
        # Agregar producto al carrito
        carrito[str(id_producto)] = {
            'nombre': producto.nombre_producto,
            'precio': str(producto.precio),
            'cantidad': 1,
            'subtotal': str(producto.precio)
        }

    request.session['carrito'] = carrito
    messages.success(request, f"Se ha agregado {producto.nombre_producto} al carrito.")
    return redirect('mostrar_productos')

# Vista para eliminar un producto del carrito
def eliminar_del_carrito(request, id_producto):
    carrito = request.session.get('carrito', {})
    if str(id_producto) in carrito:
        if carrito[str(id_producto)]['cantidad'] > 1:
            carrito[str(id_producto)]['cantidad'] -= 1
            carrito[str(id_producto)]['subtotal'] = str(
                float(carrito[str(id_producto)]['precio']) * carrito[str(id_producto)]['cantidad']
            )
        else:
            del carrito[str(id_producto)]
        request.session['carrito'] = carrito
        messages.success(request, "Producto eliminado del carrito.")
    else:
        messages.error(request, "El producto no está en el carrito.")

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
    return render(request, 'gestionproducto.html', {
        'productos': productos,
        
    })
def listar_clientes(request):
    clientes = Cliente.objects.all()  # Obtiene todos los clientes
    total_clientes = clientes.count()  # Cuenta el total de clientes
    
    # Si hay una búsqueda, filtramos los resultados
    query = request.GET.get('q', '')
    if query:
        clientes = clientes.filter(nombre_completo__icontains=query) | clientes.filter(email__icontains=query)

    return render(request, 'clientes.html', {'clientes': clientes, 'total_clientes': total_clientes, 'query': query})

def eliminar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, id_cliente=id_cliente)

    if request.method == 'POST':
        cliente.delete()
        messages.success(request, f'El cliente {cliente.nombre_completo} ha sido eliminado con éxito.')
        return redirect('listar_clientes')

    return redirect('listar_clientes')

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


def registrar_administrador(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo usuario
            form.save()
            return redirect('/registroadmin/')  # Redirigir al login después de registrar al usuario
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registroadmin.html', {'form': form})



def pedidos(request):
    # Obtener todos los pedidos junto con sus detalles
    pedidos = Pedido.objects.all().prefetch_related('detalles')
    
    return render(request, 'pedidos.html', {'pedidos': pedidos})