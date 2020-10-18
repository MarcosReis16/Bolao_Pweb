# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ApostarForm

# Create your views here.
def realizar_aposta(request):
    if request.method == 'POST':
        form = ApostarForm(request.POST)
        if not form.is_valid():

            form = ApostarForm()

    else:
        form = ApostarForm()
    context = {'form' : form}
    return render(request,'aposta.html', context)

def index(request):
    return render(request,'login.html', {})
