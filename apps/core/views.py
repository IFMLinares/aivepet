import datetime
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from allauth.account.forms import SignupForm
from apps.transactions.models import Transaction, NominalTransaccion
from .models import User


# Create your views here.

class Index(LoginRequiredMixin,ListView):
    model = Transaction
    fields = '__all__'
    template_name = 'index.html'
    context_object_name = 'ordenes'

    def get_queryset(self):
        return self.model.objects.all().order_by("start_date")

    def get_context_data(self,**kwargs):
        context = super(Index,self).get_context_data(**kwargs)

        date = datetime.date.today()

        context['load'] = (self.model.objects.filter(order_type='carga', state='En operación')).count()
        context['loadFinish'] = (self.model.objects.filter(order_type='carga', state='Finalizado')).count()
        context['totalLoad'] = context['load'] + context['loadFinish']

        context['unload'] = (self.model.objects.filter(order_type='descarga', state='En operación')).count()
        context['unloadFinish'] = (self.model.objects.filter(order_type='descarga', state='Finalizado')).count()
        context['totalUnload'] = context['unload'] + context['unloadFinish']

        context['nominalTrans'] = (NominalTransaccion.objects.filter(state='Aceptado')).count() + (NominalTransaccion.objects.filter(state='En operación')).count()
        context['nominalTransToday'] = (NominalTransaccion.objects.filter(state='Aceptado', start_date__day=date.strftime('%d'), start_date__month=date.strftime('%m'), start_date__year=date.strftime('%Y'))).count()

        context['acepted'] = (self.model.objects.filter(state='En operación')).count()
        context['total'] = context['acepted'] + context['nominalTrans']

        context['totalFinshedToday'] = (self.model.objects.filter(state='Finalizado', start_date__day=date.strftime('%d'), start_date__month=date.strftime('%m'), start_date__year=date.strftime('%Y'))).count()

        context['totalToday'] = context['totalFinshedToday'] + context['nominalTransToday']
        return context

class ListUser(LoginRequiredMixin, ListView):
    model = User
    fields = '__all__'
    template_name = 'user_list.html'
    context_object_name = 'users'

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('core:list_user')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class Developing(LoginRequiredMixin,TemplateView):
    template_name = 'developing.html'

class MyCustomSignupForm(SignupForm):

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.
        my_pass = User.objects.make_random_password()
        user.set_password(my_pass)

        message = 'Su contraseña es: %s' % (my_pass)
        body = render_to_string(
            'email_content.html',{
                'message': message
            },
        )
        email_message = EmailMessage(
            subject='REGISTRO EXITOSO',
            body = body,
            from_email= 'notificaciones@aivepet.com',
            to = [user.email]
        )
        email_message.content_subtype = 'html'
        email_message.send()

        # You must return the original result.
        return user