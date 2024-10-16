from django import views
from django.urls import path, re_path
from .views import AjaxDetallePedidoUpdateView, ClienteListView, ClienteDetailView, ClienteCreateView, \
    ClienteUpdateView, ClienteDeleteView, ConvenioModificatorioCreateView, DashboardView, cargar_mandos_preliminar, \
    confirmar_carga_mandos, PedidosPdf, PedidoPDFView
from .views import ContratoListView, ContratoDetailView, ContratoCreateView, ContratoUpdateView, ContratoDeleteView
from .views import ProductoListView, ProductoDetailView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView
from .views import PresentacionListView, PresentacionDetailView, PresentacionCreateView, PresentacionUpdateView, PresentacionDeleteView
from .views import AlmacenListView, AlmacenDetailView, AlmacenCreateView, AlmacenUpdateView, AlmacenDeleteView
from .views import PedidoCreateView,PedidoListView, PedidoDetailView, PedidoUpdateView, PedidoDeleteView,FiltrarContratosAlmacenes






urlpatterns = [

     #path('dashboard/', DashboardView.as_view(), name='dashboard'),  # Ruta para el dashboard

    # URLs para Clientes
    path('clientes/', ClienteListView.as_view(), name='cliente-list'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='cliente-detail'),
    path('clientes/nuevo/', ClienteCreateView.as_view(), name='cliente-create'),
    path('clientes/<int:pk>/editar/', ClienteUpdateView.as_view(), name='cliente-update'),
    path('clientes/<int:pk>/borrar/', ClienteDeleteView.as_view(), name='cliente-delete'),

    # URLs para Contratos
    path('contratos/', ContratoListView.as_view(), name='contrato-list'),
    path('contratos/<int:pk>/', ContratoDetailView.as_view(), name='contrato-detail'),
    path('contratos/nuevo/', ContratoCreateView.as_view(), name='contrato-create'),
    path('contratos/<int:pk>/editar/', ContratoUpdateView.as_view(), name='contrato-update'),
    path('contratos/<int:pk>/borrar/', ContratoDeleteView.as_view(), name='contrato-delete'),
    
    path('contratos/<int:contrato_id>/convenio/nuevo/', ConvenioModificatorioCreateView.as_view(), name='nuevo_convenio'),

    # URLs para Productos
    path('productos/', ProductoListView.as_view(), name='producto-list'),
    path('productos/<int:pk>/', ProductoDetailView.as_view(), name='producto-detail'),
    path('productos/nuevo/', ProductoCreateView.as_view(), name='producto-create'),
    path('productos/<int:pk>/editar/', ProductoUpdateView.as_view(), name='producto-update'),
    path('productos/<int:pk>/borrar/', ProductoDeleteView.as_view(), name='producto-delete'),

    # URLs para Presentaciones
    path('presentaciones/', PresentacionListView.as_view(), name='presentacion-list'),
    path('presentaciones/<int:pk>/', PresentacionDetailView.as_view(), name='presentacion-detail'),
    path('presentaciones/nuevo/', PresentacionCreateView.as_view(), name='presentacion-create'),
    path('presentaciones/<int:pk>/editar/', PresentacionUpdateView.as_view(), name='presentacion-update'),
    path('presentaciones/<int:pk>/borrar/', PresentacionDeleteView.as_view(), name='presentacion-delete'),

 # URLs para Pedidos
    path('pedidos/', PedidoListView.as_view(), name='pedido-list'),
    path('pedidos/nuevo/', PedidoCreateView.as_view(), name='pedido-create'),
    path('filtrar-contratos-almacenes/', FiltrarContratosAlmacenes.as_view(), name='filtrar-contratos-almacenes'),
   
    path('pedidos/<int:pk>/', PedidoDetailView.as_view(), name='pedido-detail'),
    path('pedidos/<int:pk>/eliminar/', PedidoDeleteView.as_view(), name='pedido-delete'),

    path('pedido/<int:pk>/editar/', PedidoUpdateView.as_view(), name='pedido-update'),
    path('pedido/<int:pk>/editar/detalles/', AjaxDetallePedidoUpdateView.as_view(), name='ajax-detalle-pedido-update'),
    path('pedido/<int:pk>/pdf/', PedidoPDFView.as_view(), name='pedido-pdf'),


     
    
    # URLs para Almacenes
    path('almacenes/', AlmacenListView.as_view(), name='almacen-list'),
    path('almacenes/<int:pk>/', AlmacenDetailView.as_view(), name='almacen-detail'),
    path('almacenes/nuevo/', AlmacenCreateView.as_view(), name='almacen-create'),
    path('almacenes/update/<int:pk>/', AlmacenUpdateView.as_view(), name='almacen-update'),
    path('almacenes/<int:pk>/borrar/', AlmacenDeleteView.as_view(), name='almacen-delete'),
   
    path('cargar-mandos/', cargar_mandos_preliminar, name='cargar-mandos-preliminar'),
    path('confirmar-carga-mandos/', confirmar_carga_mandos, name='confirmar-carga-mandos'),
   
 
]
    
