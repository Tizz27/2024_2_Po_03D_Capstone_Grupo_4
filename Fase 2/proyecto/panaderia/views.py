from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Producto
from .forms import ProductoForm
from .forms import ClienteForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout

from .forms import LoginForm
from .models import Cliente
from django.contrib import messages

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

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contraseña']
            
            # Intentar encontrar el cliente por su email
            try:
                cliente = Cliente.objects.get(email=email)
                
                # Verificar que la contraseña coincida (sin cifrado, en tu caso)
                if cliente.contraseña == contraseña:
                    # Si la contraseña es correcta, guardamos el 'id_cliente' en la sesión
                    request.session['cliente_id'] = cliente.id_cliente
                    
                    # Redirigimos a la página de inicio u otra página protegida
                    return redirect('home')  # Aquí puedes cambiar 'home' por la URL que desees

                else:
                    messages.error(request, 'Correo electrónico o contraseña incorrectos.')
            except Cliente.DoesNotExist:
                messages.error(request, 'Correo electrónico o contraseña incorrectos.')
    else:
        form = LoginForm()

    # Renderizamos el formulario de login en la página
    return render(request, 'login1.html', {'form': form})

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
    return render(request, 'mostrar_productos.html', {'productos': productos})

def base(request):
    return render(request, 'base.html')


def cerrar(request):
    logout(request)
    return render (request,'home.html')