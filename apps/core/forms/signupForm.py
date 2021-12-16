from django import forms
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
usuario = get_user_model()

class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        # para mostrar todos los campos del admin usar
        # fields = '__all__'
        fields = ['role',
                  'first_name',
                  'last_name',
                  'company_name',
                  'rif',
                  'direction',
                  'phone_number', ]

        labels = {
            'role': 'role',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'company_name': 'Nombre de la empresa',
            'rif': 'RIF',
            'direction': 'Dirección',
            'phone_number': 'Número de teléfono',
        }

        widgets = {
            'role': forms.TextInput(attrs={'placeholder': 'rol'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'apellido'}),
            'company_name': forms.TextInput(attrs={'placeholder': 'Nombre de la empresa'}),
            'rif': forms.TextInput(attrs={'placeholder': 'RIF'}),
            'direction': forms.TextInput(attrs={'placeholder': 'Dirección'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Número de teléfono'}),
        }

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']
        user.company_name = self.cleaned_data['company_name']
        user.rif = self.cleaned_data['rif']
        user.direction = self.cleaned_data['direction']
        user.phone_number = self.cleaned_data['phone_number']

        my_pass = usuario.objects.make_random_password()
        user.set_password(my_pass)
        user.save()
        message = 'Nombre de usuario: %s Contraseña: %s' % (user.username,my_pass)
        body = render_to_string(
            'email_content.html',{
                'message': message
            },
        )
        email_message = EmailMessage(
            subject='REGISTRO DE USUARIO EN EL SISTEMA AIVEPET',
            body = body,
            from_email= 'notificaciones@aivepet.com',
            to = [user.email]
        )
        email_message.content_subtype = 'html'
        email_message.send()
