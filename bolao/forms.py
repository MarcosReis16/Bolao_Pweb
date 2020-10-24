# -*- coding:utf-8 -*-

from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from .models import (Usuario, Aposta, Partida)
from django.utils.translation import ugettext_lazy as _


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('nome_player','login_player','password', 'is_superuser')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True
        user.is_active = True
        user.saldo_player = 10
        user.is_superuser = self.cleaned_data["is_superuser"]

        if commit:
            user.save()
        return user

class ApostarForm(forms.ModelForm):
    class Meta:
        model = Aposta
        fields = ('partida','placar_time1','placar_time2')

class CriarPartidaForm(forms.ModelForm):
    class Meta:
        model = Partida
        fields = ('nome_time1', 'nome_time2')


