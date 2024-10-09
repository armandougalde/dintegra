from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


# Create your views here.

class IndexView(TemplateView):
    template_name='index.html'
    