# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .forms import ApostarForm, UserCreationForm, CriarPartidaForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Usuario, Partida, Aposta
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404


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


def encerra_Partida(request, pk, p1, p2):
    if not request.user.is_superuser:
        raise ValidationError(_('Usuário não autorizado'), code='invalid')
    
    partida = get_object_or_404(Partida, id_partida=pk)

    partida.encerrar_partida(p1,p2)

    return HttpResponse(status=204)

def realizar_Aposta(request, pk, p1, p2):
    if request.user.is_superuser:
        raise ValidationError(_('Superusuário não realiza apostas'), code='invalid')
    
    partida = get_object_or_404(Partida, id_partida=pk)

    usuario = get_object_or_404(Usuario, id_player=request.user.pk)

    aposta = Aposta();
    aposta.apostar(p1,p2,partida,usuario)

    return HttpResponse(status=204)

def cadastrarPartida(request):
    if not request.user.is_superuser:
        raise ValidationError(_('Usuário não autorizado'), code='invalid')

    if request.method == 'POST':
        form = CriarPartidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CriarPartidaForm()
    return render(request, 'criarPartida.html', {'form': form})

def adicionar_saldo(request, pk, valor):
    if not request.user.is_superuser:
        raise ValidationError(_('Usuário não autorizado'), code='invalid')

    usuario = get_object_or_404(Usuario, id_player=pk)

    usuario.adicionar_saldo(valor);

    return HttpResponse(status=204)
    

    


