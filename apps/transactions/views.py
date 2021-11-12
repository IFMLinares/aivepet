# from django.shortcuts import render
from django.core.serializers import serialize
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from apps.transactions.models import Product, Transaction, Winerie, Destination, ReceivingCustomer, NominalTransaccion

# Create your views here.

'''
Resumen de las vistas usadas en el módulo de transacciones

Vista para el modelo de transacciones:

    AddOrder: Vista para añadir las órdenes de carga/descarga
    OrderListLoad: Listado de todas las órdenes en gestión de carga
    OrderListDownload: Listado de todas las órdenes en gestión de descarga
    OrderUpdate: Vista utilizada para el monitoreo y actualización de cualquier orden no culminada

    Las siguientes vistas son solo para el guardado de datos enviados por ajax, no tienen ningún html visible:

        WineriesAdd: Guarda las bodegas con relacion ManyToMany
        ProductAdd: Guarda los productos con relacion ManyToMany
        DestinationAdd: Guarda los destinos con relacion ManyToMany
        ReceivingCustomerAdd: Guarda los clientes recibidores con relacion ManyToMany


Vistas para el modelo de Transacciones nominales:

    AddOrderNominal: Nomina un nuevo barco Cuyo estatus por defecto es "En espera"
    NominalList: Lista de barcos nominados cuyo estatus sigue "En espera"


'''

# Añadir nueva orden carga/descarga
class AddOrder(LoginRequiredMixin,CreateView):
    model = Transaction
    fields = '__all__'
    template_name = 'add_order.html'
    success_url = '/'

# Listado de orden de carga
class OrderListLoad(LoginRequiredMixin,ListView):
    model = Transaction
    # fields = '__all__'
    template_name = 'order_list.html'
    context_object_name = 'ordenes'

    def get_queryset(self):
        return self.model.objects.filter(order_type='carga')

# Listado de orden de descarga
class OrderListDownload(LoginRequiredMixin,ListView):
    model = Transaction
    # fields = '__all__'
    template_name = 'order_list.html'
    context_object_name = 'ordenes'

    def get_queryset(self):
        return self.model.objects.filter(order_type='descarga')

class OrderListProducts(LoginRequiredMixin,ListView):
    model = Product
    fields = '__all__'
    template_name = 'list_products.html'
    context_object_name = 'products'

class OrderListCustomers(LoginRequiredMixin,ListView):
    model = Transaction
    fields = '__all__'
    template_name = 'list_customers.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return self.model.objects.all().only('customer_name')

# Actualiazación de ordenes carga/descarga
class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = '__all__'
    template_name = 'update_order.html'
    success_url = reverse_lazy('core:index')
    context_object_name = 'orden'

# Vista para añadir internamente las bodegas (no visible para el usuario, solo para registro de datos)
class WineriesAdd(LoginRequiredMixin, CreateView):
    model = Winerie

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        bodega = self.request.POST['bodega_nueva']
        producto = self.request.POST['producto']
        peso = self.request.POST['peso']
        orden = self.request.POST['transaccion']
        winerie = Winerie.objects.create(number=bodega, weight=peso, product=Product.objects.get(pk=producto))
        trans = Transaction.objects.get(order_number=orden)
        trans.Wineries.add(winerie)
        net_weight = trans.net_weight
        trans.net_weight = net_weight
        trans.save()
        query = Winerie.objects.get(pk=winerie.pk)
        producto = Product.objects.get(pk=query.product.pk)
        data = serialize('json', [query,producto])
        return HttpResponse(data, 'application/json')

# Vista para añadir internamente los productos (no visible para el usuario, solo para registro de datos)
class ProductAdd(LoginRequiredMixin, CreateView):
    model = Product

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        product = Product.objects.create(name=self.request.POST['product'])
        query = Product.objects.get(pk=product.pk)
        data = serialize('json', [query,])
        return HttpResponse(data, 'application/json')

# Vista para añadir internamente los destinos (no visible para el usuario, solo para registro de datos)
class DestinationAdd(LoginRequiredMixin, CreateView):
    model = Destination

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        destination = self.model.objects.create(destiny=self.request.POST['destino'])
        query = self.model.objects.get(pk=destination.pk)
        data = serialize('json', [query,])
        return HttpResponse(data, 'application/json')

# Vista para añadir internamente los clientees recibidores (no visible para el usuario, solo para registro de datos)
class ReceivingCustomerAdd(LoginRequiredMixin, CreateView):
    model = ReceivingCustomer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        cliente = self.model.objects.create(name=self.request.POST['cliente'])
        query = self.model.objects.get(pk=cliente.pk)
        data = serialize('json', [query,])
        return HttpResponse(data, 'application/json')

# Nominar nuevo barco
class AddOrderNominal(LoginRequiredMixin,CreateView):
    model = NominalTransaccion
    fields = '__all__'
    template_name = 'add_order_nominal.html'
    success_url = '/'

#  Lista de barcos nominados
class NominalList(LoginRequiredMixin,ListView):
    model = NominalTransaccion
    # fields = '__all__'
    template_name = 'list_nominal.html'
    context_object_name = 'ordenes'
