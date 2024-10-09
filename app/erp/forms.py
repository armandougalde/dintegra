from django import forms
from django.forms import inlineformset_factory, formset_factory
from .models import Cliente, Contrato, Convenios,  Presentacion, Producto
from .models import Pedido, DetallePedido,Almacen
from django.forms import inlineformset_factory
from .models import Pedido, DetallePedido


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['clave', 'rfc', 'nombre', 'calle', 'numero_exterior', 'numero_interior', 'colonia', 'codigo_postal', 'municipio', 'estado']
        widgets = {
            
            'clave':forms.TextInput(attrs={'class':'form-control col-md-3'}),

            'rfc':forms.TextInput(attrs={'class':'form-control col-md-3'}),
            
            'nombre':forms.TextInput(attrs={'class':'form-control col-md-12'}),
            
            'calle':forms.TextInput(attrs={'class':'form-control'}),
            
            'numero_exterior':forms.TextInput(attrs={'class':'form-control'}),
            
            'numero_interior':forms.TextInput(attrs={'class':'form-control'}),
            
            'colonia':forms.TextInput(attrs={'class':'form-control'}),
            
            'codigo_postal':forms.TextInput(attrs={'class':'form-control'}),
            
                     
            'municipio':forms.TextInput(attrs={'class':'form-control'}),

            'estado':forms.TextInput(attrs={'class':'form-control'}),
            
            
        }

class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['numero_contrato', 'descripcion', 'fecha_firma', 'fecha_inicio', 'fecha_fin', 'monto_minimo', 'monto_maximo', 'cliente']
        widgets = {
                    'numero_contrato':forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
                    'descripcion':forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
                    'fecha_firma': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                    'cliente':forms.Select(attrs={'class': 'form-control'}),
                    'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                    'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),                     
                    'monto_minimo': forms.TextInput(attrs={'class': 'form-control','choices':'settings.CURRENCY_CHOICES'}),
                    'monto_maximo': forms.TextInput(attrs={'class': 'form-control','choices':'settings.CURRENCY_CHOICES'}), 
                }
  
class ConvenioModificatorioForm(forms.ModelForm):
    class Meta:
        model = Convenios
        fields = ['tipo_convenio', 'num_convenio', 'fecha_convenio', 'monto_nuevo', 'nueva_fecha_fin', 'descripcion_adicional']
        widgets = {
            'tipo_convenio': forms.Select(attrs={'class': 'form-control'}),
            'num_convenio': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_convenio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'monto_nuevo': forms.TextInput(attrs={'class': 'form-control'}),
            'nueva_fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion_adicional': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_convenio = cleaned_data.get("tipo_convenio")

        # Validar los campos según el tipo de convenio
        if tipo_convenio == 'MONTO' and not cleaned_data.get("monto_nuevo"):
            self.add_error('monto_nuevo', 'Debes especificar el nuevo monto máximo.')
        elif tipo_convenio == 'FECHA' and not cleaned_data.get("nueva_fecha_fin"):
            self.add_error('nueva_fecha_fin', 'Debes especificar la nueva fecha de fin del contrato.')
        elif tipo_convenio == 'TEXTO' and not cleaned_data.get("descripcion_adicional"):
            self.add_error('descripcion_adicional', 'Debes proporcionar una descripción adicional.')
        
        return cleaned_data  
  
        
class ProductoForm( forms.ModelForm):
    class Meta:
        model=Producto
        fields =['nombre', 'descripcion', 'unidad_cotizacion', 'precio_unitario']
        widgets={

            'nombre':forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
            'descripcion':forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
            'unidad_cotizacion':forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
            'precio_unitario':forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
                 
                }

class PresentacionForm(forms.ModelForm):
    class Meta:
        model = Presentacion
        fields = ['nombre', 'cantidad']
        widgets={

            'nombre':forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
            'cantidad':forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
            
                 
                }

class AlmacenForm(forms.ModelForm):
    class Meta:
        model = Almacen
        fields = ['clave', 'nombre', 'calle', 'numero_exterior','responsable', 'numero_interior', 'colonia', 'codigo_postal', 'municipio', 'estado']
        widgets = {
            
            'clave':forms.TextInput(attrs={'class':'form-control col-md-3'}),            
            
            'nombre':forms.TextInput(attrs={'class':'form-control col-md-12'}),
            
            'responsable':forms.TextInput(attrs={'class':'form-control col-md-12'}),
            
            'calle':forms.TextInput(attrs={'class':'form-control'}),
            
            'numero_exterior':forms.TextInput(attrs={'class':'form-control'}),
            
            'numero_interior':forms.TextInput(attrs={'class':'form-control'}),
            
            'colonia':forms.TextInput(attrs={'class':'form-control'}),
            
            'codigo_postal':forms.TextInput(attrs={'class':'form-control'}),
                  
            
            'municipio':forms.TextInput(attrs={'class':'form-control'}),

            'estado':forms.TextInput(attrs={'class':'form-control'}),
            
            
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si necesitas inicializar algo relacionado con el cliente, asegúrate de que esté en kwargs
class PedidoForm(forms.ModelForm):
    numero_contrato = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    class Meta:
        model = Pedido
        fields = ['numero_pedido', 'fecha_solicitud', 'cliente', 'contrato', 'almacen_entrega']
        widgets = {
            'fecha_solicitud': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_pedido':forms.TextInput(attrs={'class':'form-control'}),
            'cliente':forms.Select(attrs={'class':'form-control presentacion-select'}),
            'contrato':forms.Select(attrs={'class':'form-control presentacion-select'}),
            'almacen_entrega':forms.Select(attrs={'class':'form-control presentacion-select'}),
        }
 
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
    extra=1,
    can_delete=True,
)

DetallePedidoFormSet2 = inlineformset_factory(
    Pedido,
    DetallePedido,
    form=DetallePedidoForm,
    max_num=100,
    fields= ['cantidad', 'presentacion', 'producto', 'atenciones', 'precio_unitario', 'total_litros', 'precio_presentacion', 'importe'],
    extra=0,
    can_delete=True,
)


