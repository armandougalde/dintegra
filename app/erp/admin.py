from django.contrib import admin

# Register your models here.
from .models import  Cliente, Contrato,Presentacion,Producto,Pedido,DetallePedido,Almacen


admin.site.register(Cliente)
admin.site.register(Contrato)
admin.site.register(Presentacion)
admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Almacen)
