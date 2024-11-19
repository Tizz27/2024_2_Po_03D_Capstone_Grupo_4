from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto
from .models import Cliente, Sucursal
from .models import Pedido, DetallePedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion_envio', 'fecha_entrega','comentarios']
        widgets = {
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'}),
            
        }

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