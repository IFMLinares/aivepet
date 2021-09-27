from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings

# Create your models here.

# transaction model
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    order_number = models.SlugField(max_length=200, blank=True, null=True)
    order_type = models.CharField(max_length=150, verbose_name='unidad de medida')
    number_invoice = models.PositiveIntegerField(verbose_name='Número de factura', unique=True)
    unit_measurement = models.CharField(max_length=150, verbose_name='unidad de medida')
    customer_name = models.CharField(max_length=150, verbose_name='Nombre del cliente')
    receiving_customer = models.CharField(max_length=150, verbose_name='Nombre del cliente recibidor')
    product = models.CharField(max_length=150, verbose_name='Producto')
    buque_name = models.CharField(max_length=150, verbose_name='Nombre del buque')
    port_name = models.CharField(max_length=150, verbose_name='Nombre del puerto')
    numero_muelle =  models.PositiveIntegerField(verbose_name='Número del muelle')

    def save(self, *args, **kwargs):
        id_orden = self.pk
        self.order_number = slugify('{}'.format(self.pk))
        super(Transaction, self).save(*args,**kwargs)