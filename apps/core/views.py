from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.transactions.models import Transaction

# Create your views here.

class Index(LoginRequiredMixin,ListView):
    model = Transaction
    fields = '__all__'
    template_name = 'index.html'
    context_object_name = 'ordenes'

class Developing(LoginRequiredMixin,TemplateView):
    template_name = 'developing.html'