from django import forms
from django.db.models import fields
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'username',
            'rif',
            'company_name',
            'direction',
            'phone_number',
            ]
        labels = {
            'email': 'Email',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': 'Nombre de usuario',
            'rif': 'RIF/CI',
            'company_name': 'Compañía',
            'direction': 'Dirección',
            'phone_number': 'Número de teléfono',
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control add-order mt-sm-2'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control add-order mt-sm-2'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control add-order mt-sm-2'}),
            'username': forms.TextInput(attrs={'class': 'form-control add-order mt-sm-2'}),
            'rif': forms.TextInput(attrs={'class': 'form-control add-order mt-sm-2'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control add-order mt-sm-2'}),
            'direction': forms.TextInput(attrs={'class': 'form-control add-order mt-sm-2'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control add-order mt-sm-2'}),
        }