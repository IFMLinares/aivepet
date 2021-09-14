from django import forms
from django.contrib.auth import get_user_model

class SignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        # para mostrar todos los campos del admin usar
        # fields = '__all__'
        fields = ['first_name', 'last_name']

        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder':'nombre'}),
            'last_name': forms.TextInput(attrs={'placeholder':'apellido'}),
        }

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()