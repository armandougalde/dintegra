from django import forms
from django.forms import inlineformset_factory, formset_factory
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
        widgets = {
            'fecha_solicitud':forms.TextInput(attrs={'class': 'form-control datepicker', 'autocomplete': 'off'}),
            'numero_pedido':forms.TextInput(attrs={'class':'form-control'}),
            'cliente':forms.Select(attrs={'class':'form-control presentacion-select'}),
            'contrato':forms.Select(attrs={'class':'form-control presentacion-select'}),
            'almacen_entrega':forms.Select(attrs={'class':'form-control presentacion-select'}),
        }
        

class DetallePedidoForm2(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['producto','total_litros', 'cantidad', 'presentacion', 'atenciones', 'precio_presentacion','precio_unitario', 'importe']
        

class DetallePedidoForm(forms.ModelForm):
    total_litros = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    precio_presentacion = forms.DecimalField(required=False, max_digits=10, decimal_places=2)

    class Meta:
        model = DetallePedido
        fields = ['cantidad', 'presentacion', 'producto', 'atenciones', 'precio_unitario', 'total_litros', 'precio_presentacion', 'importe']

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad') or 0
        presentacion = cleaned_data.get('presentacion')
        precio_unitario = cleaned_data.get('precio_unitario') or 0

        # Asegurar que se haya seleccionado una presentación
        if not presentacion:
            raise forms.ValidationError("Debes seleccionar una presentación.")

        # Verifica que el objeto Presentacion existe antes de intentar calcular
        if not hasattr(presentacion, 'cantidad'):
            raise forms.ValidationError("La presentación seleccionada no tiene una cantidad válida.")

        # Calcula los valores
        total_litros = cantidad * presentacion.cantidad
        precio_presentacion = precio_unitario * presentacion.cantidad
        importe = precio_presentacion * cantidad

        # Asigna los valores calculados a la instancia del modelo
        self.instance.total_litros = total_litros
        self.instance.precio_presentacion = precio_presentacion
        self.instance.importe = importe

        return cleaned_data
    



    
DetallePedidoFormSet = inlineformset_factory(
    Pedido,
    DetallePedido,
    form=DetallePedidoForm,
    max_num=100,
    fields= ['cantidad', 'presentacion', 'producto', 'atenciones', 'precio_unitario', 'total_litros', 'precio_presentacion', 'importe'],
    extra=0,
    can_delete=True,
)
