from django import forms
from django.forms import inlineformset_factory
from .models import Cliente, Contrato,Presentacion
from .models import Pedido, DetallePedido,Almacen
from django.forms import inlineformset_factory
from .models import Pedido, DetallePedido

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['clave', 'rfc', 'nombre', 'calle', 'numero_exterior', 'numero_interior', 'colonia', 'codigo_postal', 'localidad', 'municipio', 'estado']


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['numero_contrato', 'descripcion', 'fecha_firma', 'fecha_inicio', 'fecha_fin', 'monto_minimo', 'monto_maximo', 'cliente']




class PresentacionForm(forms.ModelForm):
    class Meta:
        model = Presentacion
        fields = ['nombre', 'cantidad']





class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = ['clave', 'nombre', 'calle', 'numero_exterior', 'numero_interior', 'colonia', 'codigo_postal', 'localidad', 'municipio', 'estado']
    
   # cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), widget=forms.HiddenInput(), required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['cliente'].queryset = Cliente.objects.filter(pk=self.instance.cliente.pk)
            self.fields['cliente'].widget.attrs['readonly'] = 'readonly'

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['numero_pedido', 'fecha_solicitud', 'cliente', 'contrato', 'almacen_entrega']
        

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto', 'cantidad', 'presentacion', 'atenciones', 'precio_unitario']

DetallePedidoFormSet = inlineformset_factory(
    Pedido,
    DetallePedido,
    fields=['producto', 'cantidad', 'presentacion', 'atenciones', 'precio_unitario', 'importe'],
    form=DetallePedidoForm,
    extra=1,
    can_delete=True
)

