# login/forms.py
# login/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
        username = forms.CharField(label='Nombre de Usuario')
        password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)