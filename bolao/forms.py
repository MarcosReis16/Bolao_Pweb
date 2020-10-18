# -*- coding:utf-8 -*-

from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from .models import (Usuario, Aposta, Partida, EncerrarPartida)


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome_player','login_player','password', 'groups')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True
        user.is_active = True
        user.saldo_player = 10

        if commit:
            user.save()
        return user


# class CustomUserAdmin(UserAdmin):
#     # The forms to add and change user instances
#     add_form = UserCreationForm
#     list_display = ("nome_player",)
#     ordering = ("nome_player",)

#     fieldsets = (
#         (None, {'fields': ('nome_player', 'login_player', 'saldo_player', 'groups', 'password')}),
#         )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('nome_player', 'login_player', 'saldo_player', 'password', 'groups', 'is_superuser', 'is_staff', 'is_active')}
#             ),
#         )

#     filter_horizontal = ()


class ApostarForm(forms.ModelForm):
    class Meta:
        model = Aposta
        fields = ('partida','placar_time1','placar_time2')

class CriarPartidaForm(forms.ModelForm):
    class Meta:
        model = Partida
        fields = ('nome_time1', 'nome_time2')

# class CriarPartidaAdmin(ModelAdmin):
#     add_form: CriarPartidaForm
#     fieldsets = (
#         (None, {'fields': ('nome_time1', 'nome_time2')}),
#         )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('nome_time1', 'nome_time2')}
#             ),
#         )

class EncerrarPartidaForm(forms.ModelForm):
    partida = forms.ChoiceField(choices=Partida.objects.filter(id_partida=1))
    class Meta:
        model = EncerrarPartida
        fields= ('placar_time1','placar_time2')
        readonly_fields = ('partida')
    
    def save(self, commit=True):
        partida = super(EncerrarPartidaForm, self).save(commit=False)
        fields = ('placar_time1', 'placar_time2')

        if request.method == 'POST':
            form = ContactForm(request.POST)
            if form.is_valid():

                if commit:
                    self.encerrar_partida(form.cleaned_data['placar_time1'], form.cleaned_data['placar_time2'])

            else:
                form = ContactForm()

        return partida

# class EncerrarPartidaAdmin(ModelAdmin):
#     add_form: EncerrarPartidaForm
#     fieldsets = (
#         (None, {'fields': ('placar_time1', 'placar_time2')}),
#         )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('placar_time1', 'placar_time2')}
#             ),
#         )
