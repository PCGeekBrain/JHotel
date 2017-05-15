"""Site wide views"""
from django.shortcuts import render, render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext

def view_404(request):
    render(request, '404.html')

def view_505(request):
    render(request, '500.html')
