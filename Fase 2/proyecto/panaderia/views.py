from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Producto
from .forms import ProductoForm
from .forms import ClienteForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout

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

def base(request):
    return render(request, 'base.html')