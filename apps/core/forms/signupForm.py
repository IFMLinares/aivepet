from django import forms
from django.contrib.auth import get_user_model


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
        user.save()
