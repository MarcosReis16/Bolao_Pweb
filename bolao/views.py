# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ApostarForm, UserCreationForm
from django.contrib.auth import login, authenticate

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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login_player = form.cleaned_data.get('login_player')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=login_player, password=raw_password)
            #todo
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
