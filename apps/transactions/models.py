from itertools import product
from pyexpat import model
from django.db import models
from django.db.models.fields import DateField
from django.template.defaultfilters import slugify
from django.conf import settings
from simple_history.models import HistoricalRecords
from apps.core.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Producto')
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__ (self):
        return self.name

class ProductWeight(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    weight = models.FloatField(verbose_name='Peso nominado', blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class Winerie(models.Model):
    number = models.CharField(max_length=150, verbose_name='Bodega')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    weight = models.CharField(max_length=150, verbose_name='peso')
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    remaining_in_warehouse = models.FloatField(blank=False, null=False, default=0)

    def __str__ (self):
        return self.number + self.weight

class ReceivingCustomer(models.Model):
    company_name = models.CharField(max_length=150, verbose_name='nombre de la empresa', blank=True, null=True)
    name = models.CharField(max_length=150, verbose_name='Nombre del cliente recibidor', blank=True, null=True, default='N/A')
    tipdoc = models.CharField(max_length=150, verbose_name='Documento de identificación', blank=True, null=True, default='N/A')
    dni = models.CharField(max_length=150, verbose_name='Documento de identificación', blank=True, null=True, default='N/A')
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    quantity = models.FloatField(blank=False, null=False, default=0)
    total = models.FloatField(blank=False, null=False, default=0)
    total_viajes = models.PositiveIntegerField(blank=False, null=False, default=0)

    def __str__ (self):
        return self.name

class Destination(models.Model):
    destiny = models.CharField(max_length=150, verbose_name='Destino')
    product = models.ManyToManyField(Product, blank=True)
    customer_name = models.ForeignKey(ReceivingCustomer, on_delete=models.CASCADE, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__ (self):
        return self.destiny


class Transport(models.Model):
    customer_name = models.ForeignKey(ReceivingCustomer, on_delete=models.CASCADE, blank=True, null=True)
    vehicle = models.CharField(max_length=150, verbose_name='vehículo', blank=True, null=True)
    license_plate = models.CharField(max_length=150, verbose_name='placa', blank=True, null=True)
    driver_name = models.CharField(max_length=150, verbose_name='nombre del conductor', blank=True, null=True)
    ficha = models.CharField(max_length=150, verbose_name='ficha', blank=True, null=True)
    direction = models.CharField(max_length=150, verbose_name='direccción', blank=True, null=True)
    boat_alm = models.CharField(max_length=150, verbose_name='bote/alm', blank=True, null=True)
    freight_paid_by = models.CharField(max_length=150, verbose_name='flete pagado por', blank=True, null=True)
    comment = models.CharField(max_length=150, verbose_name='comentario', blank=True, null=True)
    syndicate = models.CharField(max_length=150, verbose_name='Sindicato', blank=True, null=True)
    tank_plate = models.CharField(max_length=150, verbose_name='Placa del depósito', blank=True, null=True)
    tare_weight = models.FloatField(verbose_name='Peso de tara', blank=True, null=True)
    gross_weight = models.FloatField(verbose_name='Peso bruto', blank=True, null=True)
    net_weight = models.FloatField(verbose_name='Peso neto', blank=True, null=True)
    port = models.CharField(max_length=150, verbose_name='Puerto', blank=True, null=True)
    T_Muelle = models.CharField(max_length=150, verbose_name='Muelle', blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    viaje = models.PositiveIntegerField(blank=True, null=True, default=0)
    acumulado = models.FloatField(blank=False, null=False, default=0)
    acumulado_total = models.FloatField(blank=False, null=False, default=0)
    bodega = models.CharField(max_length=150, verbose_name='Bodega', blank=True, null=True)
    bodega_fk = models.ForeignKey(Winerie, on_delete=models.CASCADE, blank=True, null=True)
    remaining_in_warehouse_transport = models.FloatField(blank=False, null=False, default=0)

    def __str__ (self):
        return self.vehicle

class Weight(models.Model):
    gross_weight = models.CharField(max_length=150, verbose_name='peso bruto', blank=True, null=True)
    tare_weight = models.CharField(max_length=150, verbose_name='peso de tara', blank=True, null=True)
    heavy = models.CharField(max_length=150, verbose_name='pesada', blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class Status(models.Model):
    state = models.CharField(max_length=150, verbose_name='Estado', blank=True, null=True)
    comment = models.TextField(verbose_name='comentario de estatus', blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True, blank=True, null=True)

class MultipleBL(models.Model):
    bl = models.FloatField(verbose_name='Bill of Lading del buque', blank=True, null=True)
    receiving_customer = models.ForeignKey(ReceivingCustomer,on_delete=models.CASCADE, blank=True, null=True,related_name='user')
    product = models.ForeignKey(Product,on_delete=models.CASCADE, blank=True, null=True)
# transaction model
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,related_name='user')
    nominal_id = models.CharField(max_length=150, verbose_name='nominal id', blank=True, null=True)
    status = models.ManyToManyField(Status, blank=True)
    order_number = models.SlugField(max_length=200, blank=True, null=True)
    order_type = models.CharField(max_length=150, verbose_name='Tipo de orden', blank=True, null=True)
    number_invoice_client = models.CharField(max_length=150, verbose_name='Número de referencia cliente',unique=True, blank=True, null=True)
    number_invoice_aivepet = models.CharField(max_length=150, verbose_name='Número de referencia aivepet',unique=True, blank=True, null=True)
    unit_measurement = models.CharField(max_length=150, verbose_name='unidad de medida', blank=True, null=True)
    customer_name = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='customer')
    receiving_customer = models.ManyToManyField(ReceivingCustomer, blank=True)
    product = models.ManyToManyField(ProductWeight, blank=True)
    total_product_weight = models.FloatField(max_length=150, verbose_name='Total de los productos', blank=True, null=True, default=0)
    buque_name = models.CharField(max_length=150, verbose_name='Nombre del buque', blank=True, null=True)
    port_name = models.CharField(max_length=150, verbose_name='Nombre del puerto', blank=True, null=True)
    numero_muelle =  models.CharField(max_length=150,verbose_name='Número del muelle', blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    final_date = models.DateTimeField(blank=True, null=True)
    act_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    Wineries = models.ManyToManyField(Winerie,blank=True)
    net_weight = models.FloatField(verbose_name='peso neto', blank=True, null=True, default=0)
    total_weighing = models.FloatField(max_length=150, verbose_name='total de la pesada', blank=True, null=True)
    total_weight = models.FloatField(max_length=150, verbose_name='Sumatoria de todas las cargas/descargaas', blank=True, null=True, default=0)
    condition = models.CharField(max_length=150, verbose_name='condición', blank=True, null=True)
    destinations = models.ManyToManyField(Destination, blank=True)
    transport = models.ManyToManyField(Transport, blank=True)
    transport_heavy = models.CharField(max_length=150, verbose_name='Peso total del transporte', blank=True, null=True, default=0)
    state = models.CharField(max_length=150, verbose_name='Estado de la transaccion', blank=True, null=True)
    comment_initial = models.TextField(verbose_name='comentario inicial', blank=True, null=True)
    bl = models.FloatField(verbose_name='Bill of Lading del buque', blank=True, null=True, default=0)
    multiple_bl = models.ManyToManyField(MultipleBL, blank=True, default=0)
    total_bls = models.FloatField(verbose_name='total bls', blank=True, null=True, default=0)
    draft = models.FloatField(verbose_name='Draft del buque', blank=True, null=True, default=0)
    cant_carg = models.FloatField(verbose_name='Draft puerto de carga', blank=True, null=True, default=0)
    final_draft = models.CharField(max_length=150,verbose_name='Draft final', blank=True, null=True, default='0')
    company_name = models.CharField(max_length=150, verbose_name='nombre de la empresa', blank=True, null=True, default='N/A')
    name = models.CharField(max_length=150, verbose_name='Nombre del cliente recibidor', blank=True, null=True, default='N/A')
    tipdoc = models.CharField(max_length=150, verbose_name='Documento de identificación', blank=True, null=True, default='N/A')
    dni = models.CharField(max_length=150, verbose_name='Documento de identificación', blank=True, null=True, default='N/A')
    updates = models.PositiveBigIntegerField(default=0, blank=True, null=True)
    history = HistoricalRecords(inherit=True)
    difference = models.FloatField(verbose_name='diferencia', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.order_number = slugify('{}'.format(self.pk))
        super(Transaction, self).save(*args,**kwargs)

    def __str__ (self):
        return str(self.pk)


class NominalTransaccion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,related_name='user_nominal')
    total_product_weight = models.FloatField(max_length=150, verbose_name='Total de los productos', blank=True, null=True, default=0)
    order_number = models.SlugField(max_length=200, blank=True, null=True)
    order_type = models.CharField(max_length=150, verbose_name='Tipo de orden', blank=True, null=True)
    number_invoice_client = models.CharField(max_length=150, verbose_name='Número de referencia cliente',unique=True, blank=True, null=True)
    number_invoice_aivepet = models.CharField(max_length=150, verbose_name='Número de referencia aivepet',unique=True, blank=True, null=True)
    receiving_customer = models.ManyToManyField(ReceivingCustomer, blank=True)
    unit_measurement = models.CharField(max_length=150, verbose_name='unidad de medida', blank=True, null=True)
    customer_name = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='customer_nominal')
    product = models.ManyToManyField(ProductWeight, blank=True)
    buque_name = models.CharField(max_length=150, verbose_name='Nombre del buque', blank=True, null=True)
    port_name = models.CharField(max_length=150, verbose_name='Nombre del puerto', blank=True, null=True)
    numero_muelle = models.CharField(max_length=150,verbose_name='Número del muelle', blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    comment = models.TextField(verbose_name='Comentarios', blank=True, null=True)
    company_name = models.CharField(max_length=150, verbose_name='nombre de la empresa', blank=True, null=True)
    name = models.CharField(max_length=150, verbose_name='Nombre del cliente recibidor', blank=True, null=True)
    tipdoc = models.CharField(max_length=150, verbose_name='Documento de identificación', blank=True, null=True)
    dni = models.CharField(max_length=150, verbose_name='Documento de identificación', blank=True, null=True)
    state = models.CharField(max_length=150, verbose_name='Estado de la transaccion', blank=True, null=True)


    # def save(self, *args, **kwargs):
    #     self.order_number = slugify('{}'.format(self.pk))
    #     super(NominalTransaccion, self).save(*args,**kwargs)
