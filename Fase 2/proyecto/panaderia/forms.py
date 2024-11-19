from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Producto
from .models import Cliente
from .models import Pedido, DetallePedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [ 'estado', 'direccion_envio', 'fecha_entrega', 'comentarios', 'sucursal', 'total', 'cliente']
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

import datetime
import re

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_completo', 'fecha_nacimiento', 'email', 'contraseña', 'direccion', 'rut']
        widgets = {
            'contraseña': forms.PasswordInput(),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
        hoy = datetime.date.today()
        hace_100_anios = hoy.replace(year=hoy.year - 100)

        if fecha_nacimiento > hoy:
            raise forms.ValidationError("La fecha de nacimiento no puede ser futura.")
        if fecha_nacimiento < hace_100_anios:
            raise forms.ValidationError("La fecha de nacimiento no puede ser de hace más de 100 años.")
        return fecha_nacimiento

class LoginForm(forms.Form):
    email = forms.EmailField()
    contraseña = forms.CharField(widget=forms.PasswordInput)