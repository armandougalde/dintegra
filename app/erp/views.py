from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Cliente,Contrato,Producto,Presentacion,Pedido,Almacen
from .forms import ClienteForm, ContratoForm, PedidoForm, AlmacenForm,DetallePedidoFormSet,PresentacionForm
from decimal import Decimal
from django.db import transaction

class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/cliente_list.html'
    context_object_name = 'clientes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)  # Añade esta línea para depurar
        return context


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'clientes/cliente_detail.html'

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('cliente-list')

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('cliente-list')  

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente-list')

#-------------CONTRATOS---------------#




class ContratoListView(ListView):
    model = Contrato
    template_name = 'contratos/contrato_list.html'
    context_object_name = 'contratos'

class ContratoDetailView(DetailView):
    model = Contrato
    template_name = 'contratos/contrato_detail.html'
    context_object_name = 'contrato'

class ContratoCreateView(CreateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'contratos/contrato_form.html'
    success_url = reverse_lazy('contrato-list')

class ContratoUpdateView(UpdateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'contratos/contrato_form.html'
    success_url = reverse_lazy('contrato-list')

class ContratoDeleteView(DeleteView):
    model = Contrato
    template_name = 'contratos/contrato_confirm_delete.html'
    context_object_name = 'contrato'
    success_url = reverse_lazy('contrato-list')


# Vistas para Productos
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/producto_list.html'
    context_object_name = 'productos'

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/producto_detail.html'
    context_object_name = 'producto'

class ProductoCreateView(CreateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    fields = ['nombre', 'descripcion', 'unidad_cotizacion', 'precio_unitario']
    success_url = reverse_lazy('producto-list')

class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    fields = ['nombre', 'descripcion', 'unidad_cotizacion', 'precio_unitario']
    success_url = reverse_lazy('producto-list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'
    context_object_name = 'producto'
    success_url = reverse_lazy('producto-list')

# Vistas para Presentaciones
class PresentacionListView(ListView):
    model = Presentacion
    template_name = 'presentaciones/presentacion_list.html'
    context_object_name = 'presentaciones'

class PresentacionDetailView(DetailView):
    model = Presentacion
    template_name = 'presentaciones/presentacion_detail.html'
    context_object_name = 'presentacion'

class PresentacionCreateView(CreateView):
    model = Presentacion
    form_class = PresentacionForm
    template_name = 'presentaciones/presentacion_form.html'
    success_url = reverse_lazy('presentacion-list')

class PresentacionUpdateView(UpdateView):
    model = Presentacion
    template_name = 'presentaciones/presentacion_form.html'
    fields = ['tipo_presentacion', 'cantidad']
    success_url = reverse_lazy('presentacion-list')

class PresentacionDeleteView(DeleteView):
    model = Presentacion
    template_name = 'presentaciones/presentacion_confirm_delete.html'
    context_object_name = 'presentacion'
    success_url = reverse_lazy('presentacion-list')


class AlmacenListView(ListView):
    model = Almacen
    template_name = 'almacenes/almacen_list.html'
    context_object_name = 'almacenes'

class AlmacenDetailView(DetailView):
    model = Almacen
    template_name = 'almacenes/almacen_detail.html'
    context_object_name = 'almacen'

class AlmacenCreateView(CreateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'almacenes/almacen_form.html'
    success_url = reverse_lazy('almacen-list')

class AlmacenUpdateView(UpdateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'almacenes/almacen_form.html'
    success_url = reverse_lazy('almacen-list')

class AlmacenDeleteView(DeleteView):
    model = Almacen
    template_name = 'almacenes/almacen_confirm_delete.html'
    context_object_name = 'almacen'
    success_url = reverse_lazy('almacen-list')

#data['productos'] = Producto.objects.all()  # Cargar todos los productos
class PedidoCreateView(CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/pedido_form.html'
    success_url = '/pedidos/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['detalle_formset'] = DetallePedidoFormSet(self.request.POST)
        else:
            data['detalle_formset'] = DetallePedidoFormSet()
            data['productos'] = Producto.objects.all()  # Cargar todos los productos
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']

        with transaction.atomic():
            self.object = form.save()
            if detalle_formset.is_valid():
                detalles = detalle_formset.save(commit=False)
                for detalle in detalles:
                    detalle.pedido = self.object
                    detalle.save()
                detalle_formset.save_m2m()
                
                # Actualizar campos calculados
                self.object.subtotal = sum(detalle.importe for detalle in self.object.detalles.all())
                self.object.iva = self.object.subtotal * Decimal('0.16')
                self.object.total = self.object.subtotal + self.object.iva
                self.object.save()
                return redirect(self.success_url)
            else:
                print("Formset errors:", detalle_formset.errors)
                return self.render_to_response(self.get_context_data(form=form, detalle_formset=detalle_formset))

    def form_invalid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']
        print("Form errors:", form.errors)
        print("Formset errors:", detalle_formset.errors)
        return self.render_to_response(self.get_context_data(form=form, detalle_formset=detalle_formset))






class PedidoListView(ListView):
    model = Pedido
    template_name = 'pedidos/pedido_list.html'
    context_object_name = 'pedidos'
    paginate_by = 10  # Opcional, para paginar la lista si hay muchos pedidos

class PedidoDetailView(DetailView):
    model = Pedido
    template_name = 'pedidos/pedido_detail.html'  # Asegúrate de que esta plantilla exista
    context_object_name = 'pedido'  # Nombre de contexto que se utilizará en la plantilla


class PedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/pedido_form.html'
    success_url = '/pedidos/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['detalle_formset'] = DetallePedidoFormSet(self.request.POST, instance=self.object)
        else:
            data['detalle_formset'] = DetallePedidoFormSet(instance=self.object)
            data['productos'] = Producto.objects.all()  # Precargar todos los productos
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']
        if form.is_valid() and detalle_formset.is_valid():
            self.object = form.save()
            detalle_formset.instance = self.object
            detalle_formset.save()
            # Calcular subtotal, IVA y total después de guardar los detalles
            self.object.subtotal = sum([detalle.importe for detalle in self.object.detalles.all()])
            self.object.iva = self.object.subtotal * Decimal('0.16')
            self.object.total = self.object.subtotal + self.object.iva
            self.object.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form, detalle_formset=detalle_formset))

class PedidoDeleteView(DeleteView):
    model = Pedido
    template_name = 'pedidos/pedido_confirm_delete.html'
    success_url = reverse_lazy('pedido-list')