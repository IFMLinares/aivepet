import datetime
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.transactions.models import Transaction, NominalTransaccion

# Create your views here.

class Index(LoginRequiredMixin,ListView):
    model = Transaction
    fields = '__all__'
    template_name = 'index.html'
    context_object_name = 'ordenes'

    def get_context_data(self,**kwargs):
        context = super(Index,self).get_context_data(**kwargs)

        date = datetime.date.today()

        context['load'] = (self.model.objects.filter(order_type='carga', state='En operación')).count()
        context['loadFinish'] = (self.model.objects.filter(order_type='carga', state='Finalizado')).count()
        context['totalLoad'] = context['load'] + context['loadFinish']

        context['unload'] = (self.model.objects.filter(order_type='descarga', state='En operación')).count()
        context['unloadFinish'] = (self.model.objects.filter(order_type='descarga', state='Finalizado')).count()
        context['totalUnload'] = context['unload'] + context['unloadFinish']

        context['nominalTrans'] = (NominalTransaccion.objects.filter(state='En espera')).count()
        context['nominalTransToday'] = (NominalTransaccion.objects.filter(state='En espera', start_date__day=date.strftime('%d'), start_date__month=date.strftime('%m'), start_date__year=date.strftime('%Y'))).count()

        context['acepted'] = context['load'] + context['unload']
        context['total'] = context['load'] + context['unload'] + context['nominalTrans']

        context['totalFinshedToday'] = (self.model.objects.filter(state='Finalizado', start_date__day=date.strftime('%d'), start_date__month=date.strftime('%m'), start_date__year=date.strftime('%Y'))).count()
        return context

class Developing(LoginRequiredMixin,TemplateView):
    template_name = 'developing.html'
