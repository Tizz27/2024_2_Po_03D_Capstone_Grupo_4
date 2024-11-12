from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto, Pedido
from .forms import PedidoForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required

def menu(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'menu.html', data)

def productos(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, 'productos.html', data)

def sobre_nosotros(request):
    return render(request, 'sobre_nosotros.html')

def contacto(request):
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.save()
            messages.success(request, 'Pedido enviado correctamente')
            return redirect('contacto')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = PedidoForm()
    
    context = {
        'form': form,
        'productos': productos
    }
    return render(request, 'contacto.html', context)

@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    paginator = Paginator(pedidos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'lista_pedidos.html', {'page_obj': page_obj})