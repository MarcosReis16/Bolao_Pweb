# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ApostarForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Usuario, Partida
from django.utils.translation import ugettext_lazy as _

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
    if not request.user.is_superuser:
        raise ValidationError(_('Usuário não autorizado'), code='invalid')

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

def list_Users(request):
    if not request.user.is_superuser:
        raise ValidationError(_('Usuário não autorizado'), code='invalid')

    user_list = Usuario.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'listaUsuarios.html', { 'users': users })

def list_Partidas(request):
    if not request.user.is_superuser:
        raise ValidationError(_('Usuário não autorizado'), code='invalid')

    partidas = Partida.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(partidas, 10)
    try:
        partidas = paginator.page(page)
    except PageNotAnInteger:
        partidas = paginator.page(1)
    except EmptyPage:
        partidas = paginator.page(paginator.num_pages)

    return render(request, 'listaPartidas.html', { 'partidas': partidas })

