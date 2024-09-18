from django import forms
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.forms import formset_factory, inlineformset_factory
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Cliente,Contrato, DetallePedido,Producto,Presentacion,Pedido,Almacen
from .forms import ClienteForm, ContratoForm, DetallePedidoForm, PedidoForm, AlmacenForm,DetallePedidoFormSet,PresentacionForm
from decimal import Decimal
from django.http import JsonResponse
from django.contrib import messages

from django.db.models import Q
from django.db import transaction
from django.views.generic.edit import FormView

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
    fields = ['clave', 'nombre', 'calle', 'numero_exterior', 'numero_interior', 'colonia', 'codigo_postal', 'localidad', 'municipio', 'estado']
    template_name = 'almacenes/almacen_form.html'
    success_url = '/almacenes/'

    def form_valid(self, form):
        # Obtener el cliente_id de los parámetros de la URL o de la consulta
        cliente_id = self.request.GET.get('cliente_id')
        if cliente_id:
            # Asignar el cliente al formulario
            form.instance.cliente = Cliente.objects.get(pk=cliente_id)
        else:
            # Si no se encuentra el cliente_id, devolver un error de formulario inválido
            return self.form_invalid(form)
        return super().form_valid(form)

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





class PedidoCreateView(FormView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/pedido_form.html'
    success_url = '/pedidos/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        cliente_id = self.request.GET.get('cliente_id')  # Obtener el cliente seleccionado
       
        if self.request.POST:
            data['detalle_formset'] = DetallePedidoFormSet(self.request.POST)
            detalle_formset = inlineformset_factory(Pedido, DetallePedido, form=DetallePedidoForm, extra=0)(self.request.POST)
        else:
            data['detalle_formset'] = DetallePedidoFormSet()
            data['productos'] = Producto.objects.all()
            data['presentaciones'] = Presentacion.objects.all()
            detalle_formset = inlineformset_factory(Pedido, DetallePedido, form=DetallePedidoForm, extra=1)()
        data['detalle_formset'] = detalle_formset


         # Filtrar contratos y almacenes según el cliente seleccionado
        if cliente_id:
            data['contratos'] = Contrato.objects.filter(cliente_id=cliente_id)
            data['almacenes'] = Almacen.objects.filter(cliente_id=cliente_id)
        else:
            data['contratos'] = Contrato.objects.none()
            data['almacenes'] = Almacen.objects.none()


        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']
        print("Total de formularios enviados:", detalle_formset.total_form_count())  # Depuración: revisar cuántos formularios se están recibiendo

        if form.is_valid() and detalle_formset.is_valid():
            try:
                with transaction.atomic():
                    # Guardar el Pedido primero
                    self.object = form.save()
                    # Asignar la instancia del Pedido al formset
                    detalle_formset.instance = self.object
                    print(f"Cantidad de formularios en el FormSet: {len(detalle_formset.forms)}")
                    detalle_formset.save()
                      # Imprimir los datos guardados para cada formulario
                 # Guardar cada formulario del formset
                    for detalle_form in detalle_formset:
                        if detalle_form.cleaned_data:
                            detalle_form.instance.pedido = self.object
                            detalle_form.save()
                
                 # Calcular el subtotal, IVA y total después de guardar los detalles
                    self.object.subtotal = sum([detalle.importe for detalle in self.object.detalles.all()])
                    self.object.iva = self.object.subtotal * Decimal('0.16')
                    self.object.total = self.object.subtotal + self.object.iva
                    self.object.save()
                    if self.object.numero_pedido:  # O usa self.object.pk si usas el id autogenerado
                        url = reverse('pedido-detail', args=[self.object.numero_pedido])
                        return redirect(url)
                    else:
                        form.add_error(None, "No se pudo generar el número de pedido.")
                        return self.form_invalid(form)
                    
            except Exception as e:
                form.add_error(None, str(e))
                return self.form_invalid(form)
        else:
            
            return self.form_invalid(form)
        




class PedidoListView(ListView):
    model = Pedido
    template_name = 'pedidos/pedido_list.html'
    context_object_name = 'pedidos'
    paginate_by = 10  # Opcional, para paginar la lista si hay muchos pedidos
    

class PedidoDetailView(DetailView):
    model = Pedido
    template_name = 'pedidos/pedido_detail.html'  # Asegúrate de que esta plantilla exista
    context_object_name = 'pedido'  # Nombre de contexto que se utilizará en la plantilla


            
class PedidoUpdateView2(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/pedido_update2.html'
    success_url = reverse_lazy('pedido-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pedido = self.object
        cliente_id = pedido.cliente_id

        if self.request.POST:
            data['detalle_formset'] = DetallePedidoFormSet(self.request.POST, instance=pedido)
        else:
            data['detalle_formset'] = DetallePedidoFormSet(instance=pedido)
            data['productos'] = Producto.objects.all()
            data['presentaciones'] = Presentacion.objects.all()

        data['contratos'] = Contrato.objects.filter(cliente_id=cliente_id)
        data['almacenes'] = Almacen.objects.filter(cliente_id=cliente_id)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']

        if form.is_valid() and detalle_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.save()  # Guarda el pedido primero para asegurar la relación

            # Guarda todos los detalles
            detalle_formset.instance = self.object
            for detalle_form in detalle_formset:
                if detalle_form.cleaned_data.get('DELETE', False):
                    if detalle_form.instance.pk:
                        detalle_form.instance.delete()
                else:
                    detalle = detalle_form.save(commit=False)
                    detalle.pedido = self.object
                    detalle.save()

            # Recalcula el subtotal, IVA y total
            self.object.subtotal = sum([detalle.importe for detalle in self.object.detalles.all()])
            self.object.iva = self.object.subtotal * Decimal('0.16')
            self.object.total = self.object.subtotal + self.object.iva
            self.object.save()

            return redirect(self.success_url)
        else:
            print("Errores en el formulario principal:", form.errors)
            print("Errores en el FormSet:", detalle_formset.errors)
            return self.render_to_response(self.get_context_data(form=form, detalle_formset=detalle_formset))




class PedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/pedido_update2.html'
    success_url = reverse_lazy('pedido-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pedido = self.object

        if self.request.POST:
            data['detalle_formset'] = DetallePedidoFormSet(self.request.POST, instance=pedido)
        else:
            data['detalle_formset'] = DetallePedidoFormSet(instance=pedido)
            data['productos'] = Producto.objects.all()
            data['presentaciones'] = Presentacion.objects.all()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        detalle_formset = context['detalle_formset']

        if form.is_valid() and detalle_formset.is_valid():
            # Guarda el pedido primero
            self.object = form.save()

            # Debug: revisar los datos de cada formulario del formset
            for detalle_form in detalle_formset:
                print(detalle_form.cleaned_data)  # Verifica que los datos de la presentación estén presentes

            # Guardar cada detalle del formset
            for detalle_form in detalle_formset:
                if detalle_form.cleaned_data.get('DELETE', False):
                    if detalle_form.instance.pk:
                        detalle_form.instance.delete()
                else:
                    detalle = detalle_form.save(commit=False)
                    if not detalle.presentacion:
                        return JsonResponse({
                            'success': False,
                            'errors': {'presentacion': 'Debe seleccionar una presentación para cada producto'}
                        })
                    detalle.pedido = self.object  # Asociar el detalle con el pedido
                    detalle.save()

            # Calcular y guardar los totales del pedido
            self.object.subtotal = sum([detalle.importe for detalle in self.object.detalles.all()])
            self.object.iva = self.object.subtotal * Decimal('0.16')
            self.object.total = self.object.subtotal + self.object.iva
            self.object.save()

            return JsonResponse({'success': True}) if self.request.headers.get('x-requested-with') == 'XMLHttpRequest' else super().form_valid(form)
        else:
            return JsonResponse({
                'success': False,
                'errors': detalle_formset.errors
            }) if self.request.headers.get('x-requested-with') == 'XMLHttpRequest' else super().form_invalid(form)


class AjaxDetallePedidoUpdateView(View):
    def post(self, request, *args, **kwargs):
        pedido = get_object_or_404(Pedido, pk=kwargs['pk'])
        detalle_formset = DetallePedidoFormSet(request.POST, instance=pedido)

        if detalle_formset.is_valid():
            detalle_formset.save()
            response = {'status': 'success', 'message': 'Detalles guardados correctamente.'}
        else:
            response = {'status': 'error', 'message': 'Error al guardar los detalles.', 'errors': detalle_formset.errors}
        
        return JsonResponse(response)
















        





class PedidoDeleteView(DeleteView):
    model = Pedido
    template_name = 'pedidos/pedido_confirm_delete.html'
    success_url = reverse_lazy('pedido-list')

    def get_object(self, queryset=None):
        """Sobrescribe para obtener el objeto Pedido utilizando numero_pedido"""
        pk = self.kwargs.get('pk')
        return Pedido.objects.get(numero_pedido=pk)



class FiltrarContratosAlmacenes(View):
    def get(self, request, *args, **kwargs):
        cliente_id = request.GET.get('cliente_id')
        contratos = Contrato.objects.filter(cliente_id=cliente_id).values('id', 'numero_contrato')
        almacenes = Almacen.objects.filter(cliente_id=cliente_id).values('id', 'nombre')
        return JsonResponse({
            'contratos': list(contratos),
            'almacenes': list(almacenes)
        })


def filtrar_contratos_almacenes(request):
    cliente_id = request.GET.get('cliente_id')
    contratos = Contrato.objects.filter(cliente_id=cliente_id).values('id', 'numero_contrato')
    almacenes = Almacen.objects.filter(cliente_id=cliente_id).values('id', 'nombre')
    return JsonResponse({'contratos': list(contratos), 'almacenes': list(almacenes)})


