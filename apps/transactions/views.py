# from django.shortcuts import render
from asyncio.trsock import TransportSocket
from itertools import product
import os
from django.contrib import messages
from django.core.serializers import serialize
from django.conf import settings
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect, HttpResponseRedirectBase
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.contrib.staticfiles import finders
from django.shortcuts import render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
import datetime
from xhtml2pdf import pisa

from .models import Product, ProductWeight, Transaction, Winerie, Destination, ReceivingCustomer, NominalTransaccion, Transport, Weight, Status, MultipleBL
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

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

# Añadir nueva orden carga/descarga
class AddOrder(LoginRequiredMixin,CreateView):
    model = Transaction
    fields = '__all__'
    template_name = 'add_order.html'
    success_url = '/'
    context_object_name = 'query'

    def get_success_url(self):
        if(self.object.order_type == 'carga'):
            return reverse_lazy('transactions:transaction_success')
        else:
            return reverse_lazy('transactions:transaction_success')

    def get_context_data(self, **kwargs):
        ctx = super(AddOrder, self).get_context_data(**kwargs)
        # ctx['query'] = Product.objects.values('name', 'pk').distinct().order_by('name')
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
class OrderUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = '__all__'
    template_name = 'update_order.html'
    # success_url = reverse_lazy('core:index')
    context_object_name = 'orden'
    success_message = 'Cambios guardados exitosamente'

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
        remaining_in_warehouse = float(peso)

        winerie = Winerie.objects.create(number=bodega, weight=peso, product=Product.objects.get(pk=producto), remaining_in_warehouse=remaining_in_warehouse)
        trans = Transaction.objects.get(order_number=orden)
        trans.Wineries.add(winerie)
        trans.save()
        query = Winerie.objects.get(pk=winerie.pk)
        producto = Product.objects.get(pk=query.product.pk)
        data = serialize('json', [query,producto])
        return HttpResponse(data, 'application/json')


class WineriesDelete(LoginRequiredMixin, CreateView):
    model = Winerie

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        id = self.request.POST['id_bodega']
        winerie = Winerie.objects.get(pk=id)
        winerie.delete()
        winerie.save()
        # trans = Transaction.Wineries.delete(id)
        # print(trans)
        # winerie.delete()
        return ('Bodega eliminada')
        

# Vista para añadir internamente los productos (no visible para el usuario, solo para registro de datos)
class ProductAdd(LoginRequiredMixin, CreateView):
    model = Product

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        p = self.request.POST['product']
        p = p.lower()
        p = normalize(p)
        w = self.request.POST['weight']
        product, created = Product.objects.get_or_create(name=p)
        query = ProductWeight.objects.create(product_id=product, weight=w)
        data = serialize('json', [query,product])
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

class StatusAdd(LoginRequiredMixin, CreateView):
    model = Status

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        status = self.model.objects.create(
            state = self.request.POST['status_select'],
            comment = self.request.POST['status_comment'],
            fecha = self.request.POST['status_date']
        )
        query = self.model.objects.get(pk=status.pk)
        data = serialize('json', [query])
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
        transaction = get_object_or_404(Transaction, pk=trans['transaction_id'])
        viaje = 1
        if transaction.transport.count() > 0:
            viaje = transaction.transport.all().last().viaje + 1


        id_driver_name = trans['id_driver_name']
        id_freight_paid_by = trans['id_freight_paid_by']
        id_comment = trans['id_comment']

        if(id_driver_name == '' or ' ' ):
            id_driver_name = 'N/A'

        if(id_freight_paid_by == '' or ' ' ):
            id_freight_paid_by = 'N/A'

        if(id_comment == '' or ' ' ):
            id_comment = 'N/A'
        customer = ReceivingCustomer.objects.get(pk=trans['id_transport_customer'])
        winerie = Winerie.objects.get(pk=trans['id_bodega_transport'])
        remaining_in_warehouse_transport = float(winerie.weight) - float(trans['id_net_weight'])
        winerie.remaining_in_warehouse = abs(remaining_in_warehouse_transport)
        winerie.save()
        transport = self.model.objects.create(
            vehicle= trans['id_vehicle'],
            license_plate= trans['id_license_plate'],
            driver_name= id_driver_name,
            ficha= trans['id_ficha'],
            direction= trans['id_direction'],
            boat_alm= trans['id_boat_alm'],
            freight_paid_by= id_freight_paid_by,
            comment= id_comment,
            syndicate= trans['id_syndicate'],
            tank_plate= trans['id_tank_plate'],
            port= trans['id_port'],
            T_Muelle= trans['id_T_Muelle'],
            gross_weight = trans['id_gross_weight'],
            tare_weight = trans['id_tare_weight'],
            net_weight = trans['id_net_weight'],
            customer_name = customer,
            viaje = viaje,
            bodega = winerie.number,
            bodega_fk = winerie,
            remaining_in_warehouse_transport = remaining_in_warehouse_transport,
            )
        print(trans['id_bodega_transport'])
        quantity = 0
        quantity = quantity + customer.quantity  
        customer.quantity = float(quantity) + float(transport.net_weight)
        customer.save()
        query = self.model.objects.get(pk=transport.pk)
        query.customer_name = customer
        data = serialize('json', [query, customer])
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
        name = self.request.POST['cliente']
        if name == '' or name == ' ':
            name = 'N/A'
        
        dni = self.request.POST['dni']
        if dni == '' or dni == ' ':
            dni = 'N/A'
        cliente = self.model.objects.create(
            company_name=self.request.POST['empresa'],
            name=name,
            dni=dni,
            )
        query = self.model.objects.get(pk=cliente.pk)
        data = serialize('json', [query,])
        return HttpResponse(data, 'application/json')

class MultipleBLAdd(LoginRequiredMixin, CreateView):
    model = MultipleBL

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request, *args, **kwargs):
        receiving_customer = ReceivingCustomer.objects.get(id=self.request.POST['id_bl_customer'])
        product = Product.objects.get(id=self.request.POST['id_bl_product'])
        bl = self.model.objects.create(
            bl=self.request.POST['id_bl_multiple'],
            receiving_customer=receiving_customer,
            product=product,
        )
        query = self.model.objects.get(pk=bl.pk)
        data = serialize('json', [query,receiving_customer, product])
        return HttpResponse(data, 'application/json')

class UserViewTransaction(LoginRequiredMixin,DetailView):
    model = Transaction
    template_name = 'user_view_order.html'
    context_object_name = 'orden'
    
    def get_context_data(self, **kwargs):
        ctx = super(UserViewTransaction, self).get_context_data(**kwargs)
        print(ctx['orden'].pk)
        transaction = Transaction.objects.get(pk=ctx['orden'].pk)
        if transaction.order_type == 'descarga':
            try:
                a1 = float(transaction.transport_heavy) - float(transaction.total_bls)
                ctx['a1'] = a1
            except:
                ctx['a1'] = 0
            try:
                b = float(transaction.transport_heavy) - float(transaction.total_product_weight)
                ctx['b'] = b
            except:
                ctx['b'] = 0
                
            try:
                c = float(transaction.transport_heavy) - float(transaction.draft)
                ctx['c'] = c
            except:
                ctx['c'] = 0
            try:
                d = float(transaction.total_product_weight) - float(transaction.draft)
                ctx['d'] = d
            except:
                ctx['d'] = 0
        else:
            try:
                f = float(transaction.cant_carg) - float(transaction.total_product_weight)
                ctx['f'] = f
            except:
                ctx['f'] = 0
        return ctx


# Nominar nuevo barco
class AddOrderNominal(LoginRequiredMixin,CreateView):
    model = NominalTransaccion
    fields = '__all__'
    template_name = 'add_order_nominal.html'
    success_url = reverse_lazy('transactions:transaction_success')
    context_object_name = 'query'
    def get_context_data(self, **kwargs):
        ctx = super(AddOrderNominal, self).get_context_data(**kwargs)
        # ctx['products'] = Product.objects.values('name', 'pk').distinct().order_by('name')
        try:
            ctx['users'] = User.objects.all()
        except:
            pass
        return ctx

class TranssaccionSuccess(LoginRequiredMixin, TemplateView):
    template_name = 'transaction_success.html'

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

class PDFView(View):

    def link_callback(self, uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('pdf/pdf.html')
            transaction = Transaction.objects.get(pk=self.kwargs['pk'])
            total_w = 0
            for winerie in transaction.Wineries.all():
                total_w += float(winerie.weight)
                # pass
            transports = transaction.transport.all()
            receiving_customers = transaction.receiving_customer.all()
            acumulado = {}
            viajes = {}
            for receiving_customer in receiving_customers:
                acumulado[receiving_customer.company_name] = 0
                viajes[receiving_customer.company_name] = 0
            # print (acumulado)
            for transport in transports:
                # print(acumulado[transport.customer_name.company_name])
                v = viajes[transport.customer_name.company_name]
                viajes[transport.customer_name.company_name] = transport.viaje + v
                a = acumulado[transport.customer_name.company_name]
                acumulado[transport.customer_name.company_name] = a + transport.net_weight
                transport.acumulado = 0
                transport.acumulado = acumulado[transport.customer_name.company_name]
                transport.save()
            for receiving_customer in receiving_customers:
                receiving_customer.total = acumulado[receiving_customer.company_name]
                receiving_customer.total_viajes = viajes[receiving_customer.company_name]
                receiving_customer.save()
                
            quantity_darft = float(transaction.final_draft) - float(transaction.draft)
            transaction.difference = float(transaction.total_bls) - float(quantity_darft)
            transaction.save()
            if transaction.order_type == 'descarga':
                cant_desp = float(transaction.transport_heavy)
                bl_pc = float(transaction.total_bls)
                draft_pc = float(transaction.total_product_weight)
                draft_pd = float(transaction.draft) - float(transaction.final_draft)
                context = {
                    'orden': transaction,
                    'icon': '{}{}'.format(settings.STATIC_URL, 'images/logo.png'),
                    'total_w': total_w,
                    'quantity_darft': quantity_darft,
                    'a': (float(cant_desp - bl_pc)),
                    '1p': (((cant_desp - bl_pc)/bl_pc)*100),
                    'b': (cant_desp - draft_pc),
                    '2p': (((cant_desp - draft_pc)/draft_pc)*100),
                    'c': (cant_desp - draft_pd),
                    '3p': (((cant_desp - draft_pd)/draft_pd)*100),
                    'd': (draft_pc - draft_pd),
                    '4p': (((draft_pc - draft_pd)/draft_pd)*100),
                    'cant_desp': cant_desp,
                    'bl_pc': bl_pc,

                    }
                
                print(context)
            else:
                f = float(transaction.total_bls) -  float(transaction.cant_carg) 
                fp = (f /float(transaction.cant_carg) )*100
                context = {
                    'orden': transaction,
                    'icon': '{}{}'.format(settings.STATIC_URL, 'images/logo.png'),
                    'total_w': total_w,
                    'f': f,
                    'quantity_darft': quantity_darft,
                    'fp': fp,
                    }

            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        except:
            return response
        return HttpResponseRedirect(reverse_lazy('core:index'))

class PDFView1(View):

    def link_callback(self, uri, rel):
            """
            Convert HTML URIs to absolute system paths so xhtml2pdf can access those
            resources
            """
            result = finders.find(uri)
            if result:
                    if not isinstance(result, (list, tuple)):
                            result = [result]
                    result = list(os.path.realpath(path) for path in result)
                    path=result[0]
            else:
                    sUrl = settings.STATIC_URL        # Typically /static/
                    sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                    mUrl = settings.MEDIA_URL         # Typically /media/
                    mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                    if uri.startswith(mUrl):
                            path = os.path.join(mRoot, uri.replace(mUrl, ""))
                    elif uri.startswith(sUrl):
                            path = os.path.join(sRoot, uri.replace(sUrl, ""))
                    else:
                            return uri

            # make sure that file exists
            if not os.path.isfile(path):
                    raise Exception(
                            'media URI must start with %s or %s' % (sUrl, mUrl)
                    )
            return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('pdf/pdf2.html')
            transaction = Transaction.objects.get(pk=self.kwargs['pk'])
            total_w = 0
            for winerie in transaction.Wineries.all():
                total_w += float(winerie.weight)
            transports = transaction.transport.all()
            receiving_customers = transaction.receiving_customer.all()
            acumulado = {}
            viajes = {}
            for receiving_customer in receiving_customers:
                acumulado[receiving_customer.company_name] = 0
                viajes[receiving_customer.company_name] = 0
            a_total = 0
            for transport in transports:
                a_total += transport.net_weight
                v = viajes[transport.customer_name.company_name]
                viajes[transport.customer_name.company_name] = transport.viaje + v
                a = acumulado[transport.customer_name.company_name]
                acumulado[transport.customer_name.company_name] = a + transport.net_weight
                transport.acumulado = 0
                transport.acumulado = acumulado[transport.customer_name.company_name]
                transport.acumulado_total = a_total
                transport.save()
            

            for receiving_customer in receiving_customers:
                receiving_customer.total = acumulado[receiving_customer.company_name]
                receiving_customer.total_viajes = viajes[receiving_customer.company_name]
                receiving_customer.save()
            transaction.difference = float(transaction.final_draft) - float(transaction.net_weight)
            transaction.total_weight = a_total
            transaction.save()
            context = {
                'orden': transaction,
                'icon': '{}{}'.format(settings.STATIC_URL, 'images/logo.png'),
                'total_w': total_w,
                }

            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        except:
            return response
        return HttpResponseRedirect(reverse_lazy('core:index'))

def FinishTransaction(request,pk):
    transaction = Transaction.objects.get(pk=pk)
    transaction.state = 'Finalizado'
    transaction.final_date = datetime.datetime.now()
    transaction.save()
    
    transaction_nominal = NominalTransaccion.objects.get(pk=transaction.nominal_id)
    transaction_nominal.state = 'Finalizado'
    transaction_nominal.save()
    messages.success(request, 'Orden finalizada exitosamente')
    if transaction.order_type == 'carga':
        return redirect('transactions:order_list_load')
    else:
        return redirect('transactions:order_list_download')


def NominalTransAcepted(request, pk):
    nominal = NominalTransaccion.objects.filter(pk=pk)[0]
    nominal.state = 'En operación'
    nominal.save()

    transaction = Transaction(
        pk = pk,
        user = nominal.user,
        order_number = nominal.order_number,
        total_product_weight = nominal.total_product_weight,
        order_type = nominal.order_type,
        number_invoice_client = nominal.number_invoice_client,
        number_invoice_aivepet = nominal.number_invoice_aivepet,
        unit_measurement = nominal.unit_measurement,
        buque_name = nominal.buque_name,
        port_name = nominal.port_name,
        numero_muelle = nominal.numero_muelle,
        start_date = nominal.start_date,
        state = nominal.state,
        customer_name = nominal.customer_name,
        comment_initial = nominal.comment,
        company_name = nominal.company_name,
        name = nominal.name,
        tipdoc = nominal.tipdoc,
        dni = nominal.dni,
        nominal_id = str(pk)
    )
    product = nominal.product
    # customer_name = nominal.customer_name
    # product = Product.objects.get(pk=nominal.product.pk)
    # transaction.customer_name.add(customer_name)
    transaction.save()
    for p in nominal.product.all():
        transaction.product.add(p)
    transaction.save()
    for p in nominal.receiving_customer.all():
        transaction.receiving_customer.add(p)
    transaction.save()
    messages.success(request, 'Orden Aceptada exitosamente')
    return redirect('transactions:update_order', transaction.pk)

