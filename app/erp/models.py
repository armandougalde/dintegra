from django.db import models
from dal import autocomplete


class Cliente(models.Model):
    clave = models.CharField(max_length=20, unique=True)
    rfc = models.CharField(max_length=13, unique=True)
    nombre = models.CharField(max_length=255)
    calle = models.CharField(max_length=255)
    numero_exterior = models.CharField(max_length=10)
    numero_interior = models.CharField(max_length=10, blank=True, null=True)
    colonia = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=5)   
    municipio = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre






class Contrato(models.Model):
    numero_contrato = models.CharField(max_length=18, unique=True)
    descripcion = models.CharField(max_length=100)
    fecha_firma = models.DateField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    monto_minimo = models.DecimalField(max_digits=14, decimal_places=2)
    monto_maximo = models.DecimalField(max_digits=14, decimal_places=2)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.numero_contrato




class Convenios(models.Model):
    TIPO_CONVENIO_CHOICES = [
        ('MONTO', 'Aumento de Monto Máximo'),
        ('FECHA', 'Extensión de Fecha de Fin'),
        ('TEXTO', 'Cambio de Texto/Descripción')
    ]
    
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE, related_name='convenios')
    num_convenio = models.CharField(max_length=15, unique=True)
    tipo_convenio = models.CharField(max_length=10, choices=TIPO_CONVENIO_CHOICES)
    fecha_convenio = models.DateField()
    monto_nuevo = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    nueva_fecha_fin = models.DateField(null=True, blank=True)
    descripcion_adicional = models.TextField(null=True, blank=True)
    
    def aplicar_convenio(self):
        # Aplicar el convenio al contrato original según el tipo de convenio
        if self.tipo_convenio == 'MONTO' and self.monto_nuevo:
            self.contrato.monto_maximo = self.monto_nuevo
        elif self.tipo_convenio == 'FECHA' and self.nueva_fecha_fin:
            self.contrato.fecha_fin = self.nueva_fecha_fin
        elif self.tipo_convenio == 'TEXTO' and self.descripcion_adicional:
            self.contrato.descripcion += f" | Modificación: {self.descripcion_adicional}"
        
        # Guardar los cambios en el contrato
        self.contrato.save()

    def __str__(self):
        return f"Convenio {self.tipo_convenio} para {self.contrato.numero_contrato}"





class Producto(models.Model):

    
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    unidad_cotizacion = models.CharField(max_length=10)
    precio_unitario = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return self.nombre

class Presentacion(models.Model):
    
    nombre = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre

class MandoNaval(models.Model):
    clave = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True, null=True,max_length=100)
    
    

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = 'Mando Naval'
        verbose_name_plural = 'Mandos Navales'


class Almacen(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='almacenes')
    clave = models.CharField(max_length=20)
    nombre = models.CharField(max_length=255)
    calle = models.CharField(max_length=255)
    numero_exterior = models.CharField(max_length=10)
    numero_interior = models.CharField(max_length=10, blank=True, null=True)
    colonia = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=5)
    responsable = models.CharField(max_length=50)    
    municipio = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    mando = models.ForeignKey('MandoNaval', on_delete=models.CASCADE,default=1, related_name='almacenes')

    def __str__(self):
        return f"{self.nombre} ({self.clave})"


class Pedido(models.Model):
    
    numero_pedido = models.CharField(max_length=20, null=False)  # No es clave primaria, solo un campo normal
    fecha_solicitud = models.DateField()
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)
    almacen_entrega = models.ForeignKey('Almacen', on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    class Meta:
        unique_together = ('numero_pedido', 'contrato')  # Mantener esta restricción
   

   
    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.cliente}"
    



class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')  # Relación con Pedido
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    presentacion = models.ForeignKey('Presentacion', on_delete=models.CASCADE, blank=False, null=False)  # Asegurarse de que no sea nulo
    atenciones = models.TextField(blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    total_litros = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    precio_presentacion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Verificar si la presentación está definida
        if self.presentacion:
            # Calcular el total de litros
            self.total_litros = self.cantidad * self.presentacion.cantidad
            # Calcular el precio por presentación
            self.precio_presentacion = self.precio_unitario * self.presentacion.cantidad
            # Calcular el importe
            self.importe = self.cantidad * self.precio_presentacion
        else:
            self.total_litros = 0
            self.precio_presentacion = 0
            self.importe = 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle de {self.pedido.numero_pedido}"