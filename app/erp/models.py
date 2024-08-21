from django.db import models
from djmoney.models.fields import MoneyField
from decimal import Decimal

class Estado(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    nombre = models.CharField(max_length=255)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Localidad(models.Model):
    nombre = models.CharField(max_length=255)
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


from django.db import models

class Cliente(models.Model):
    clave = models.CharField(max_length=20, unique=True)
    rfc = models.CharField(max_length=13, unique=True)
    nombre = models.CharField(max_length=255)
    calle = models.CharField(max_length=255)
    numero_exterior = models.CharField(max_length=10)
    numero_interior = models.CharField(max_length=10, blank=True, null=True)
    colonia = models.CharField(max_length=255)
    codigo_postal = models.CharField(max_length=5)
    localidad = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre






class Contrato(models.Model):
    numero_contrato = models.CharField(max_length=20, unique=True)
    descripcion = models.TextField()
    fecha_firma = models.DateField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    monto_minimo = MoneyField(max_digits=14, decimal_places=2, default_currency='MXN')
    monto_maximo = MoneyField(max_digits=14, decimal_places=2, default_currency='MXN')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.numero_contrato
    




class Producto(models.Model):
    UNIDADES_CHOICES = [
        ('LITRO', 'Litro'),
        ('KILO', 'Kilo'),
        ('PIEZA', 'Pieza'),
    ]
    
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    unidad_cotizacion = models.CharField(max_length=10, choices=UNIDADES_CHOICES)
    precio_unitario = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return self.nombre

class Presentacion(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre


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
    localidad = models.CharField(max_length=255)
    municipio = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} ({self.clave})"


class Pedido(models.Model):
    numero_pedido = models.CharField(max_length=10, unique=True, editable=False)
    fecha_solicitud = models.DateField()
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    contrato = models.ForeignKey('Contrato', on_delete=models.CASCADE)
    almacen_entrega = models.ForeignKey('Almacen', on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    iva = models.DecimalField(default=0.00,max_digits=14, decimal_places=2)
    total = models.DecimalField(default=0.00,max_digits=14, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.subtotal = sum([detalle.importe for detalle in self.detalles.all()])
        self.iva = self.subtotal * Decimal('0.16')
        self.total = self.subtotal + self.iva
        
        if not self.numero_pedido:
            # Generar un número de pedido secuencial
            last_pedido = Pedido.objects.all().order_by('id').last()
            if not last_pedido:
                self.numero_pedido = 'PED0001'
            else:
                last_pedido_number = int(last_pedido.numero_pedido.split('PED')[-1])
                self.numero_pedido = 'PED' + str(last_pedido_number + 1).zfill(4)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.cliente}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    presentacion = models.ForeignKey('Presentacion', on_delete=models.CASCADE)
    atenciones = models.CharField(max_length=50)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    importe = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.importe = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)