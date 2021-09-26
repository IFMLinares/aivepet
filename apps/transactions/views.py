from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.transactions.models import Transaction

# Create your views here.
class AddOrder(LoginRequiredMixin,CreateView):
    model = Transaction
    fields = '__all__'
    template_name = 'add_order.html'
    success_url = '/transactions/'

# Create your views here.
class OrderList(LoginRequiredMixin,ListView):
    model = Transaction
    # fields = '__all__'
    template_name = 'order_list.html'
    context_object_name = 'ordenes'


