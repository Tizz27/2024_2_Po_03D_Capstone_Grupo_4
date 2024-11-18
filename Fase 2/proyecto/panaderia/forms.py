from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto
from .models import Cliente, Sucursal
from .models import Pedido, DetallePedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion_envio', 'sucursal', 'fecha_pedido', 'estado', 'cliente']

    direccion_envio = forms.CharField(max_length=255, required=False)
    sucursal = forms.ModelChoiceField(queryset=Sucursal.objects.all(), required=False)
    fecha_pedido = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    estado = forms.CharField(initial="Pendiente", widget=forms.HiddenInput())
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), widget=forms.HiddenInput(), required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': 'readonly'}), required=False)

    def __init__(self, *args, **kwargs):
        cliente = kwargs.get('cliente', None)
        super().__init__(*args, **kwargs)
        if cliente:
            # Establecer valores predeterminados para el cliente logueado
            self.fields['direccion_envio'].initial = cliente.direccion
            self.fields['email'].initial = cliente.email


class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['cantidad', 'producto']

    cantidad = forms.IntegerField(min_value=1)
    producto = forms.ModelChoiceField(queryset=Producto.objects.all())
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model= User
        fields= ['username', "first_name","email", "password1", "password2"]        

class ProductoForm(forms.ModelForm):
    
    class Meta:
        model =Producto
        fields = '__all__'

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_completo', 'fecha_nacimiento', 'email', 'contraseña', 'direccion', 'rut']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'contraseña': forms.PasswordInput(),
        }

class LoginForm(forms.Form):
    email = forms.EmailField()
    contraseña = forms.CharField(widget=forms.PasswordInput)