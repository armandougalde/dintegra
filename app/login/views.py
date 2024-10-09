# login/views.py
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.shortcuts import redirect, render
from django.views.generic import FormView,RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from erp.models import Contrato



class DatosView(LoginRequiredMixin, View):
    model = Contrato
    template_name = 'dashboard/dashboard.html'
    context_object_name = 'contratos'





       
        
class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Iniciar Sesión'
        return context

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)  # Esto redirigirá a success_url

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')  # Redirigir a dashboard si ya está autenticado
        return super().dispatch(request, *args, **kwargs)

   
        
class LogoutRedirect(RedirectView):
    pattern_name='login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
    
    
    
