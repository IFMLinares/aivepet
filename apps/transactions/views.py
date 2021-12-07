# from django.shortcuts import render
from django.core.serializers import serialize
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from .models import Product, Transaction, Winerie, Destination, ReceivingCustomer, NominalTransaccion, Transport
from apps.core.models import User

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
    context_object_name = 'query'

    def get_success_url(self):
        if(self.object.order_type == 'carga'):
            return reverse_lazy('transactions:order_list_load')
        else:
            return reverse_lazy('transactions:order_list_download')

    def get_context_data(self, **kwargs):
        ctx = super(AddOrder, self).get_context_data(**kwargs)
        ctx['query'] = Product.objects.values('name', 'pk').distinct().order_by('name')
        try:
            ctx['users'] = User.objects.all()
        except:
            pass
        return ctx


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
    model = ReceivingCustomer
    fields = '__all__'
    template_name = 'list_customers.html'
    context_object_name = 'customers'

    def get_queryset(self):
        return self.model.objects.all()

# Actualiazación de ordenes carga/descarga
class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = '__all__'
    template_name = 'update_order.html'
    # success_url = reverse_lazy('core:index')
    context_object_name = 'orden'

    def get_success_url(self):
        if(self.object.order_type == 'carga'):
            return reverse_lazy('transactions:order_list_load')
        else:
            return reverse_lazy('transactions:order_list_download')


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
        # trans = Transaction.objects.get(order_number=orden)
        # trans.Wineries.add(winerie)
        # net_weight = trans.net_weight
        # trans.net_weight = net_weight
        # trans.save()
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
        customer = ReceivingCustomer.objects.get(pk=self.request.POST['customer'])
        product =  Product.objects.get(pk=self.request.POST['product'])
        destination = self.model.objects.create(
            destiny=self.request.POST['destino'],
            customer_name = customer,
        )
        destination.product.add(product)
        query = self.model.objects.get(pk=destination.pk)
        user = ReceivingCustomer.objects.get(pk = query.customer_name.pk)
        # product = Product.objects.get(pk = query.product.pk)
        data = serialize('json', [query, user, product])
        return HttpResponse(data, 'application/json')

class GetAct(LoginRequiredMixin, CreateView):
    model = Transaction

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        query = self.model.objects.filter(pk=self.request.POST['id']).first()
        s = query.history.all()
        # history = query.history.all()
        # product = Product.objects.get(pk = query.product.pk)
        data = serialize('json', [query])
        return HttpResponse(data, 'application/json')

# Vista para añadir internamente los transportes (no visible para el usuario, solo para registro de datos)
class TransportAdd(LoginRequiredMixin, CreateView):
    model = Transport

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        trans = self.request.POST
        transport = self.model.objects.create(
            transport_weight= trans['id_transport_weight'],
            vehicle= trans['id_vehicle'],
            license_plate= trans['id_license_plate'],
            driver_name= trans['id_driver_name'],
            ficha= trans['id_ficha'],
            direction= trans['id_direction'],
            boat_alm= trans['id_boat_alm'],
            balance= trans['id_balance'],
            freight_paid_by= trans['id_freight_paid_by'],
            comment= trans['id_comment'],
            )
        query = self.model.objects.get(pk=transport.pk)
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
        cliente = self.model.objects.create(
            company_name=self.request.POST['empresa'],
            name=self.request.POST['cliente'],
            dni=self.request.POST['dni'],
            tipdoc= self.request.POST['tipodc']
            )
        query = self.model.objects.get(pk=cliente.pk)
        data = serialize('json', [query,])
        return HttpResponse(data, 'application/json')

class UserViewTransaction(LoginRequiredMixin,DetailView):
    model = Transaction
    template_name = 'user_view_order.html'
    context_object_name = 'orden'

# Nominar nuevo barco
class AddOrderNominal(LoginRequiredMixin,CreateView):
    model = NominalTransaccion
    fields = '__all__'
    template_name = 'add_order_nominal.html'
    success_url = '/'
    context_object_name = 'query'
    def get_context_data(self, **kwargs):
        ctx = super(AddOrderNominal, self).get_context_data(**kwargs)
        ctx['products'] = Product.objects.values('name', 'pk').distinct().order_by('name')
        try:
            ctx['users'] = User.objects.all()
        except:
            pass
        return ctx

#  Lista de barcos nominados
class NominalList(LoginRequiredMixin,ListView):
    model = NominalTransaccion
    # fields = '__all__'
    template_name = 'list_nominal.html'
    context_object_name = 'ordenes'

class NominalTransactionDelete(DeleteView):
    model = NominalTransaccion
    success_url = reverse_lazy('transactions:order_list_nominal')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class NominalTransactionDetail(LoginRequiredMixin,DetailView):
    model = NominalTransaccion
    template_name = 'detail_nominal.html'
    context_object_name = 'orden'


def NominalTransAcepted(request, pk):
    nominal = NominalTransaccion.objects.filter(pk=pk)[0]
    nominal.state = 'Aceptado'
    nominal.save()

    transaction = Transaction(
        user = nominal.user,
        order_number = nominal.order_number,
        order_type = nominal.order_type,
        number_invoice = nominal.number_invoice,
        unit_measurement = nominal.unit_measurement,
        buque_name = nominal.buque_name,
        port_name = nominal.port_name,
        numero_muelle = nominal.numero_muelle,
        start_date = nominal.start_date,
        state = nominal.state,
        customer_name = nominal.customer_name
    )
    product = nominal.product
    # customer_name = nominal.customer_name
    # product = Product.objects.get(pk=nominal.product.pk)
    # transaction.customer_name.add(customer_name)
    transaction.save()
    for p in nominal.product.all():
        transaction.product.add(p)
    transaction.save()
    return redirect('transactions:order_list_nominal')