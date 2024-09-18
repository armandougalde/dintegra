from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

class CustomLoginView(LoginView):
    template_name = 'login/login.html'  # Tu plantilla de login
    success_url = reverse_lazy('home')  # La vista a la que redirigir después de iniciar sesión

    def form_valid(self, form):
        # Aquí puedes agregar lógica personalizada si es necesario
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login') 

@login_required
def home_view(request):
    return render(request, 'login/templates/home.html')