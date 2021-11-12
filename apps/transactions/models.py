from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Producto')
    def __str__ (self):
        return self.name

class Winerie(models.Model):
    number = models.CharField(max_length=150, verbose_name='Bodega')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    weight = models.CharField(max_length=150, verbose_name='Bodega')
    def __str__ (self):
        return self.number + self.weight

class Destination(models.Model):
    destiny = models.CharField(max_length=150, verbose_name='Destino')

    def __str__ (self):
        return self.destiny

class ReceivingCustomer(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre del cliente recibidor', blank=True, null=True)

    def __str__ (self):
        return self.name

# transaction model
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    order_number = models.SlugField(max_length=200, blank=True, null=True)
    order_type = models.CharField(max_length=150, verbose_name='unidad de medida', blank=True, null=True)
    number_invoice = models.PositiveIntegerField(verbose_name='Número de factura', unique=True , blank=True, null=True)
    unit_measurement = models.CharField(max_length=150, verbose_name='unidad de medida', blank=True, null=True)
    customer_name = models.CharField(max_length=150, verbose_name='Nombre del cliente', blank=True, null=True)
    receiving_customer = models.ManyToManyField(ReceivingCustomer, blank=True)
    product = models.ManyToManyField(Product, blank=True)
    buque_name = models.CharField(max_length=150, verbose_name='Nombre del buque', blank=True, null=True)
    port_name = models.CharField(max_length=150, verbose_name='Nombre del puerto', blank=True, null=True)
    numero_muelle =  models.PositiveIntegerField(verbose_name='Número del muelle', blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    Wineries = models.ManyToManyField(Winerie, blank=True)
    gross_weight = models.CharField(max_length=150, verbose_name='peso bruto', blank=True, null=True)
    net_weight = models.CharField(max_length=150, verbose_name='peso neto', blank=True, null=True)
    tare_weight = models.CharField(max_length=150, verbose_name='peso de tara', blank=True, null=True)
    heavy = models.CharField(max_length=150, verbose_name='pesada', blank=True, null=True)
    total_weighing = models.CharField(max_length=150, verbose_name='total de la pesada', blank=True, null=True)
    condition = models.CharField(max_length=150, verbose_name='condición', blank=True, null=True)
    destinations = models.ManyToManyField(Destination, blank=True)
    transport_weight = models.CharField(max_length=150, verbose_name='peso del transporte', blank=True, null=True)
    transport_heavy = models.CharField(max_length=150, verbose_name='Pesada del transporte', blank=True, null=True)
    vehicle = models.CharField(max_length=150, verbose_name='vehículo', blank=True, null=True)
    license_plate = models.CharField(max_length=150, verbose_name='placa', blank=True, null=True)
    driver_name = models.CharField(max_length=150, verbose_name='nombre del conductor', blank=True, null=True)
    ficha = models.CharField(max_length=150, verbose_name='ficha', blank=True, null=True)
    direction = models.CharField(max_length=150, verbose_name='direccción', blank=True, null=True)
    boat_alm = models.CharField(max_length=150, verbose_name='bote/alm', blank=True, null=True)
    balance = models.CharField(max_length=150, verbose_name='balanza', blank=True, null=True)
    freight_paid_by = models.CharField(max_length=150, verbose_name='flete pagado por', blank=True, null=True)
    comment = models.CharField(max_length=150, verbose_name='comentario', blank=True, null=True)
    state = models.CharField(max_length=150, verbose_name='Estado de la transaccion', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.order_number = slugify('{}'.format(self.pk))
        super(Transaction, self).save(*args,**kwargs)

    def __str__ (self):
        return str(self.pk)

class NominalTransaccion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    order_number = models.SlugField(max_length=200, blank=True, null=True)
    customer_name = models.CharField(max_length=150, verbose_name='Nombre del cliente', blank=True, null=True)
    origin_order = models.CharField(max_length=150, verbose_name='Origen de la orden', blank=True, null=True)
    buque_name = models.CharField(max_length=150, verbose_name='Nombre del buque', blank=True, null=True)
    product = models.ManyToManyField(Product, blank=True)
    state = models.CharField(max_length=150, verbose_name='Estado de la transaccion', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.order_number = slugify('{}'.format(self.pk))
        super(NominalTransaccion, self).save(*args,**kwargs)

    def __str__ (self):
        return self.pk