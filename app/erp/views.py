import http
from lib2to3.fixes.fix_input import context
from tempfile import template

from django import forms
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.forms import formset_factory, inlineformset_factory
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.template import TemplateDoesNotExist
from django.urls import  reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,TemplateView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from dal import autocomplete
from django.core.paginator import Paginator

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


from app import settings
from .models import Cliente,Contrato,Convenios, DetallePedido, MandoNaval,  Producto,Presentacion,Pedido,Almacen,Producto, Presentacion
from .forms import ClienteForm, ContratoForm, ConvenioModificatorioForm, DetallePedidoForm, DetallePedidoFormSet2, ExcelUploadForm, PedidoForm, AlmacenForm,DetallePedidoFormSet,PresentacionForm, ProductoForm
from decimal import Decimal
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage


from django.views import View
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from django.db.models import Q

from django.views.generic.edit import FormView



class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard/dashboard.html'

    def get(self, request):
        contratos = Contrato.objects.all()  # Obtén todos los contratos
        contratos_con_totales = []
        
        for contrato in contratos:
            # Obtén todos los pedidos relacionados con este contrato
            pedidos = Pedido.objects.filter(contrato=contrato)  # Asegúrate de que el modelo Pedido tenga la relación correcta
            total_pedidos = sum(pedido.total for pedido in pedidos)  # Suma los totales de los pedidos

            # Calcular monto por ejercer (monto máximo - total de pedidos)
            monto_por_ejercer = contrato.monto_maximo - total_pedidos

            # Añadir el contrato y los totales al diccionario
            contratos_con_totales.append({
                'contrato': contrato,
                'total_pedidos': total_pedidos,
                'monto_por_ejercer': monto_por_ejercer
            })

        context = {
            'contratos_con_totales': contratos_con_totales,  # Pasa los contratos con totales y monto por ejercer al contexto
        }

        return render(request, self.template_name, context)

    
    
 # Vistas para Clientes   


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.object  # Obtiene el cliente actual
        context['almacenes'] = Almacen.objects.filter(cliente=cliente)  # Filtra almacenes para el cliente
        return context
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('cliente-list')

    def form_invalid(self, form):
        print("Errores del formulario:", form.errors)
        return super().form_invalid(form)

class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('cliente-list')  

class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente-list')

# Vistas para Contratos

class ContratoListView(ListView):
    model = Contrato
    template_name = 'contratos/contrato_list.html'
    context_object_name = 'contratos'

class ContratoDetailView(DetailView):
    model = Contrato
    template_name = 'contratos/contrato_detail.html'
    context_object_name = 'contrato'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contrato = self.object

        # Filtra los clientes asociados a este contrato
        context['clientes'] = Cliente.objects.filter(contrato=contrato)

        # Obtiene los convenios asociados a este contrato
        context['convenios'] = contrato.convenios.all()  # Usar related_name para obtener los convenios

        return context

class ContratoCreateView(CreateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'contratos/contrato_form.html'
    success_url = reverse_lazy('contrato-list')

    def form_invalid(self, form):
        print("Errores del formulario:", form.errors)
        return super().form_invalid(form)
        
class ContratoUpdateView(UpdateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'contratos/contrato_form.html'
    success_url = reverse_lazy('contrato-list')

    def get_initial(self):
        initial = super().get_initial()
        # Obtener el contrato actual y asegurar que las fechas estén en formato correcto
        contrato = self.object
        
        # Formatear los montos con separadores de comas y dos decimales
        initial['monto_minimo'] = "{:,.2f}".format(contrato.monto_minimo)
        initial['monto_maximo'] = "{:,.2f}".format(contrato.monto_maximo)

        if contrato.fecha_firma:
            initial['fecha_firma'] = contrato.fecha_firma.strftime('%Y-%m-%d')
        if contrato.fecha_inicio:
            initial['fecha_inicio'] = contrato.fecha_inicio.strftime('%Y-%m-%d')
        if contrato.fecha_fin:
            initial['fecha_fin'] = contrato.fecha_fin.strftime('%Y-%m-%d')

        return initial
    
 

class ContratoDeleteView(DeleteView):
    model = Contrato
    template_name = 'contratos/contrato_confirm_delete.html'
    context_object_name = 'contrato'
    success_url = reverse_lazy('contrato-list')

#Vistas para convenios modificatorios.

class ConvenioModificatorioCreateView(CreateView):
    model = Convenios
    form_class = ConvenioModificatorioForm
    template_name = 'convenios/convenio_form.html'
    context_object_name = 'convenio'
    
    def get_initial(self):
        # Obtener el tipo de convenio desde los parámetros de la URL
        tipo_convenio = self.request.GET.get('tipo')
        initial = super().get_initial()
        if tipo_convenio:
            initial['tipo_convenio'] = tipo_convenio
        return initial
    
    def form_valid(self, form):
        contrato_id = self.kwargs['contrato_id']
        contrato = Contrato.objects.get(pk=contrato_id)
        
        # Asignar el contrato al nuevo convenio
        form.instance.contrato = contrato
        
        # Guardar el convenio y aplicar los cambios al contrato
        convenio = form.save()
        convenio.aplicar_convenio()
        
        return super().form_valid(form)
    
    def get_success_url(self):
        # Redirigir a la vista de detalle del contrato después de agregar el convenio
        return reverse_lazy('contrato-detail', kwargs={'pk': self.kwargs['contrato_id']})





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
    form_class = ProductoForm
    success_url = reverse_lazy('producto-list')

class ProductoUpdateView(UpdateView):
    model = Producto
    template_name = 'productos/producto_form.html'
    form_class = ProductoForm
    success_url = reverse_lazy('producto-list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'productos/producto_confirm_delete.html'  # Asegúrate de que la plantilla existe
    success_url = reverse_lazy('producto-list')  # Ajusta esto según tu configuración de URLs

    def get_object(self, queryset=None):
        # Obtiene el objeto Producto
        producto = super().get_object(queryset)
        
              
        return producto



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
    form_class = PresentacionForm
    success_url = reverse_lazy('presentacion-list')

class PresentacionDeleteView(DeleteView):
    model = Presentacion
    template_name = 'presentaciones/presentacion_confirm_delete.html'
    context_object_name = 'presentacion'
    success_url = reverse_lazy('presentacion-list')


# Vistas para alamacenes
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

    def get_success_url(self):
        # Redirige a la lista de clientes después de crear el almacén
        return reverse_lazy('cliente-list')

    def form_valid(self, form):
        # Obtener el cliente_id de los parámetros de la URL o de la consulta
        cliente_id = self.request.GET.get('cliente_id')
        if cliente_id:
            # Asignar el cliente al formulario
            form.instance.cliente = Cliente.objects.get(pk=cliente_id)
        else:
            messages.error(self.request, "Cliente no encontrado. No se puede guardar el almacén.")
            return self.form_invalid(form)

        # Mostrar mensaje de éxito
        messages.success(self.request, "Almacén guardado correctamente.")
        response = super().form_valid(form)

        # Redireccionar y mantener los mensajes usando HttpResponseRedirect
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request, "Error al guardar el almacén. Revisa los campos e intenta nuevamente.")
        return super().form_invalid(form)

class AlmacenUpdateView(UpdateView):
    model = Almacen
    form_class = AlmacenForm
    template_name = 'almacenes/almacen_form.html'
    success_url = reverse_lazy('almacen-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Actualizar'
        return context

class AlmacenDeleteView(DeleteView):
    model = Almacen
    template_name = 'almacenes/almacen_confirm_delete.html'
    context_object_name = 'almacen'
    success_url = reverse_lazy('almacen-list')



# Vistas para Pedidos           
class PedidoCreateView(View):
    def get(self, request):
        pedido_form = PedidoForm()
        detalle_formset = DetallePedidoFormSet(queryset=DetallePedido.objects.none())
        productos = Producto.objects.all()  
        presentaciones = Presentacion.objects.all()  

        # Obtener contrato_id de los parámetros de la URL
        contrato_id = request.GET.get('contrato_id')
        if contrato_id:
            contrato = get_object_or_404(Contrato, id=contrato_id)
            pedido_form.fields['contrato'].initial = contrato
            pedido_form.initial['numero_contrato'] = contrato.numero_contrato  # Prellenar el número de contrato

            

        return render(request, 'pedidos/pedido_form.html', {
            'pedido_form': pedido_form,
            'detalle_formset': detalle_formset,
            'productos': productos,
            'presentaciones': presentaciones,
        })

    def post(self, request):
        pedido_form = PedidoForm(request.POST)
        detalle_formset = DetallePedidoFormSet(request.POST)

        if pedido_form.is_valid() and detalle_formset.is_valid():
            try:
                pedido = pedido_form.save()  # Guardar el pedido

                # Guardar los detalles
                for detalle_form in detalle_formset:
                    detalle = detalle_form.save(commit=False)
                    detalle.pedido = pedido  # Asignar el pedido
                    detalle.save()
                    
                        # Calcular subtotal, IVA y total
                    pedido.subtotal = sum([detalle.importe for detalle in pedido.detalles.all()])
                    pedido.iva = pedido.subtotal * Decimal('0.16')
                    pedido.total = pedido.subtotal + pedido.iva
                    pedido.save()  # Guarda los cambios en el pedido

                return redirect('pedido-list')  # Redirigir a donde necesites

              

            except Exception as e:
                messages.error(request, f"Error al guardar el pedido: {str(e)}")

        # Volver a cargar los productos y presentaciones en caso de error
        return render(request, 'pedidos/pedido_form.html', {
            'pedido_form': pedido_form,
            'detalle_formset': detalle_formset,
            'productos': Producto.objects.all(),
            'presentaciones': Presentacion.objects.all(),
        })

class PedidoCreateView2(View):
    def get(self, request):
        pedido_form = PedidoForm()
        detalle_formset = DetallePedidoFormSet(queryset=DetallePedido.objects.none())
        productos = Producto.objects.all()
        presentaciones = Presentacion.objects.all()
        contrato_id = request.GET.get('contrato_id')
        if contrato_id:
            contrato = get_object_or_404(Contrato, id=contrato_id)
            pedido_form.fields['contrato'].initial = contrato
            pedido_form.initial['numero_contrato'] = contrato.numero_contrato

        return render(request, 'pedidos/pedido_form.html', {
            'pedido_form': pedido_form,
            'detalle_formset': detalle_formset,
            'productos': productos,
            'presentaciones': presentaciones,
        })

    def post(self, request):
        pedido_form = PedidoForm(request.POST)
        detalle_formset = DetallePedidoFormSet(request.POST)

        if pedido_form.is_valid() and detalle_formset.is_valid():
            try:
                pedido = pedido_form.save()  # Guardar el pedido

                # Guardar los detalles
                for detalle_form in detalle_formset:
                    detalle = detalle_form.save(commit=False)
                    detalle.pedido = pedido  # Asignar el pedido
                    detalle.save()

                # Calcular subtotal, IVA y total
                pedido.subtotal = sum([detalle.importe for detalle in pedido.detalles.all()])
                pedido.iva = pedido.subtotal * Decimal('0.16')
                pedido.total = pedido.subtotal + pedido.iva
                pedido.save()  # Guarda los cambios en el pedido

                # Enviar la actualización al grupo de WebSocket
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    "dashboard",
                    {
                        'type': 'dashboard_update',
                        'data': {
                            'contrato_id': pedido.contrato.id,
                            'total_pedidos': pedido.contrato.pedidos.aggregate(total=sum('total'))['total'],
                            'descripcion': pedido.contrato.descripcion,
                            'monto_minimo': pedido.contrato.monto_minimo,
                            'monto_maximo': pedido.contrato.monto_maximo
                        }
                    }
                )

                return redirect('pedido-list')  # Redirigir a donde necesites

            except Exception as e:
                messages.error(request, f"Error al guardar el pedido: {str(e)}")

        # Volver a cargar los productos y presentaciones en caso de error
        return render(request, 'pedidos/pedido_form.html', {
            'pedido_form': pedido_form,
            'detalle_formset': detalle_formset,
            'productos': Producto.objects.all(),
            'presentaciones': Presentacion.objects.all(),
        })
            
class PedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedidos/pedido_update.html'
    success_url = reverse_lazy('pedido-list')
    
    def get_initial(self):
        initial = super().get_initial()
        # Obtener el contrato actual y asegurar que las fechas estén en formato correcto
        pedido = self.object

        if pedido.fecha_solicitud:
            initial['fecha_solicitud'] = pedido.fecha_solicitud.strftime('%Y-%m-%d')
        

        return initial

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        pedido = self.object
        cliente_id = pedido.cliente_id

        if self.request.POST:
            data['detalle_formset'] = DetallePedidoFormSet2(self.request.POST, instance=pedido)
        else:
            data['detalle_formset'] = DetallePedidoFormSet2(instance=pedido, queryset=pedido.detalles.all())  # Mostrar solo los detalles existentes
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

from django.views.generic import ListView
from django.db.models import Prefetch
from .models import Pedido, Contrato, Cliente  # Asegúrate de tener los modelos importados

class PedidoListView2(ListView):
    model = Pedido
    template_name = 'pedidos/pedido_list.html'
    context_object_name = 'pedidos'

    def get_queryset(self):
        return Pedido.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener todos los contratos
        contratos = Contrato.objects.all()
        
        # Preparar la estructura para agrupar por contrato y luego por cliente
        contratos_con_clientes = {}
        for contrato in contratos:
            # Obtener todos los clientes relacionados con el contrato
            clientes = Cliente.objects.filter(pedido__contrato=contrato).distinct()

            # Crear la estructura para cada contrato, con clientes y pedidos (inicialmente vacío)
            contratos_con_clientes[contrato.id] = {
                'contrato': contrato,
                'clientes': {
                    cliente.id: {'cliente': cliente, 'pedidos': []} for cliente in clientes
                }
            }

        # Obtener todos los pedidos para incluirlos en la estructura anterior
        pedidos = Pedido.objects.all()

        # Agrupar los pedidos dentro de cada contrato y cliente correspondiente
        for pedido in pedidos:
            contrato_id = pedido.contrato.id
            cliente_id = pedido.cliente.id

            if contrato_id in contratos_con_clientes:
                if cliente_id in contratos_con_clientes[contrato_id]['clientes']:
                    contratos_con_clientes[contrato_id]['clientes'][cliente_id]['pedidos'].append(pedido)

        context['contratos'] = contratos_con_clientes  # Pasar los contratos con clientes al contexto
        context['hay_contratos'] = bool(contratos)  # Variable para indicar si hay contratos disponibles

        return context


class PedidoListView(ListView):
    model = Pedido
    template_name = 'pedidos/pedido_list.html'
    context_object_name = 'pedidos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener todos los contratos
        contratos = Contrato.objects.all()
        
        # Preparar la estructura para agrupar por contrato y luego por cliente
        contratos_con_clientes = {}
        for contrato in contratos:
            # Obtener todos los clientes relacionados con el contrato
            clientes = Cliente.objects.filter(pedido__contrato=contrato).distinct()

            # Crear la estructura para cada contrato, con clientes y pedidos (inicialmente vacío)
            contratos_con_clientes[contrato.id] = {
                'contrato': contrato,
                'clientes': {
                    cliente.id: {'cliente': cliente, 'pedidos': []} for cliente in clientes
                }
            }

            # Obtener todos los pedidos de este contrato, ordenados por numero_pedido
            pedidos = Pedido.objects.filter(contrato=contrato).order_by('-numero_pedido')

            # Paginación específica para este contrato
            paginator = Paginator(pedidos, 10)  # Mostramos 10 pedidos por página
            page_number = self.request.GET.get(f'page_{contrato.id}', 1)
            page_obj = paginator.get_page(page_number)

            # Añadir la paginación al contexto del contrato
            contratos_con_clientes[contrato.id]['page_obj'] = page_obj

        context['contratos'] = contratos_con_clientes  # Pasar los contratos con clientes al contexto
        context['hay_contratos'] = bool(contratos)  # Variable para indicar si hay contratos disponibles

        return context

     
class PedidoDetailView(DetailView):
    model = Pedido
    template_name = 'pedidos/pedido_detail.html'  # Asegúrate de que esta plantilla exista
    context_object_name = 'pedido'  # Nombre de contexto que se utilizará en la plantilla

class PedidoPDFView(View):
    def get(self, request, *args, **kwargs):
        pedido_id = self.kwargs.get('pk')  # Obtener el ID del pedido
        pedido = Pedido.objects.get(pk=pedido_id)  # Obtener el objeto Pedido

        # Renderiza la plantilla HTML
        html_string = render_to_string('pedidos/pedido_pdf.html', {'pedido': pedido})
        
        # Convierte el HTML a PDF
        pdf = HTML(string=html_string).write_pdf()
        
        # Devuelve el PDF como respuesta
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="pedido_{pedido.numero_pedido}.pdf"'
        return response

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

import pandas as pd # type: ignore




def cargar_mandos_preliminar(request):
    print("Solicitud recibida en cargar_mandos_preliminar")
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print("Formulario válido, procesando archivo...")
            excel_file = request.FILES.get("excel_file")
            if not excel_file:
                messages.error(request, "No se seleccionó ningún archivo. Intenta de nuevo.")
                print("No se seleccionó ningún archivo.")
                return redirect("cargar-mandos-preliminar")

            try:
                # Leer el archivo Excel usando pandas sin encabezado
                print("Leyendo el archivo Excel...")
                df = pd.read_excel(excel_file, header=None, engine='openpyxl')
                print("Archivo leído correctamente.")

                if df.empty:
                    messages.error(request, "El archivo Excel está vacío. Verifica el contenido.")
                    print("El archivo Excel está vacío.")
                    return redirect("cargar-mandos-preliminar")

                # Asignar nombres personalizados a las columnas
                print("Procesando y asignando nombres a las columnas...")
                df.columns = ['clave', 'descripcion']
                df = df.dropna(subset=['clave', 'descripcion'])  # Eliminar filas vacías

                # Guardar el DataFrame en la sesión para su confirmación posterior
                request.session['preliminar_data'] = df.to_dict(orient='records')
                print("Datos guardados en la sesión:", request.session['preliminar_data'])

                # Intentar renderizar la plantilla preliminar_mandos.html
                print("Intentando renderizar la plantilla preliminar_mandos.html...")
                try:
                    return render(request, "preliminar_mandos.html", {"data": df.to_dict(orient='records')})
                except TemplateDoesNotExist as e:
                    print(f"Plantilla no encontrada: {e}")
                    return HttpResponse(f"Plantilla no encontrada: {e}")

            except pd.errors.ParserError:
                messages.error(request, "El archivo no se pudo procesar. Verifica el formato del archivo Excel.")
                print("Error de formato en el archivo.")
            except Exception as e:
                messages.error(request, f"Error en la carga del archivo: {str(e)}")
                print(f"Error en la carga del archivo: {str(e)}")
                return redirect("cargar-mandos-preliminar")
    else:
        print("Método de solicitud no es POST.")
        form = ExcelUploadForm()

    return render(request, "carga_datos.html", {"form": form})


def confirmar_carga_mandos(request):
    print("Solicitud recibida en confirmar_carga_mandos")
    preliminar_data = request.session.get('preliminar_data', [])

    if not preliminar_data:
        print("No se encontraron datos en la sesión. Redirigiendo a cargar-mandos-preliminar.")
        messages.error(request, "No se encontraron datos para cargar. Por favor, sube el archivo de nuevo.")
        return redirect("cargar-mandos-preliminar")

    # Confirmar y guardar los datos en la base de datos
    try:
        for row in preliminar_data:
            MandoNaval.objects.update_or_create(
                clave=row['clave'],
                defaults={"descripcion": row['descripcion']}
            )
        messages.success(request, "Los datos se cargaron correctamente en la base de datos.")
        print("Datos guardados exitosamente.")
    except Exception as e:
        messages.error(request, f"Error al guardar los datos: {str(e)}")

    # Limpiar los datos de la sesión
    request.session.pop('preliminar_data', None)

    return redirect("cargar-mandos-preliminar")


class PedidosPdf(View):
    def get(self, request, pk, *args, **kwargs):
        # Obtener el pedido correspondiente por su pk
        try:
            pedido = Pedido.objects.get(pk=pk)
            detalles = pedido.detalles.all()  # Usar 'detalles' debido al related_name en DetallePedido

            # Imprimir los detalles en la consola para verificar que se están obteniendo correctamente
            print("Detalles del Pedido:", detalles)  # Esto mostrará los detalles en la consola
        except Pedido.DoesNotExist:
            return HttpResponse('El pedido no existe')



        # Preparar el contexto con el pedido y sus detalles
        context = {
            'pedido': pedido,
            'detalles': detalles  # Pasar los detalles al contexto
        }

        # Renderizar la plantilla HTML a un string
        html = render_to_string('pedidos/pedido_pdf.html', context)

        # Crear una respuesta PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pedido.numero_pedido}.pdf"'

        # Crear el PDF con pisa
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Si hay errores, mostrar mensaje de error
        if pisa_status.err:
            return HttpResponse('Hubo un error al generar el PDF')

        return response


