# login/urls.py
from django.urls import path
from erp.views import  DashboardView
from login.views import LoginFormView,LogoutRedirect

urlpatterns = [
   

    path('', LoginFormView.as_view(),name="login"),
    path('logout/', LogoutRedirect.as_view(),name="logout"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    #path('datos/', DatosView.as_view(), name='datos'),

]
 