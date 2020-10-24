from djmoney.models.fields import MoneyField
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .user_manager import UserManager
from django.core.exceptions import ValidationError
from moneyed import Money


class Usuario(AbstractBaseUser, PermissionsMixin):
    id_player= models.AutoField(primary_key=True)
    nome_player = models.CharField(max_length=200, blank= False, verbose_name="Nome Completo")
    login_player = models.CharField(max_length=50, unique =True, blank= False, verbose_name="Login")
    saldo_player = MoneyField(default=Money(amount='0', currency='BRL'), max_digits=10,decimal_places=2,default_currency='BRL', verbose_name="Saldo")
    total_ganho = MoneyField(default=Money(amount='0', currency='BRL'), max_digits=10,decimal_places=2,default_currency='BRL', verbose_name="Valor total ganho")
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'),default=False)
    position = 0
    
    objects = UserManager()

    USERNAME_FIELD = 'login_player'
    REQUIRED_FIELDS = ['nome_player']

    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')

    def cadastrar(self, using):
        self.saldo_player = Money(amount='10', currency='BRL')
        self.save(using=using)

    def diminuir_saldo(self):
        valor = Money(amount='5', currency='BRL')
        self.saldo_player -= valor
        self.save()
    
    def receber_premiacao(self, valor):
        self.saldo_player += valor
        self.total_ganho += valor
        self.save()
    
    def devolver_valor(self):
        valor = Money(amount='5', currency='BRL')
        self.saldo_player += valor
        self.save()
    
    def adicionar_saldo(self, valor):
        valor = Money(amount=valor, currency='BRL')
        self.saldo_player += valor
        self.save()
    
    def obter_ranking(self):
        user_list = Usuario.objects.filter(is_superuser = False).order_by('-total_ganho','login_player')
        for index, user in enumerate(user_list):
            user.position = index + 1
        return user_list

    def __str__(self):
        return self.nome_player
    
class Partida(models.Model):
    id_partida = models.AutoField(primary_key=True)
    nome_time1 = models.CharField(max_length=100, blank= False, verbose_name="Time 1")
    placar_time1 = models.IntegerField(default=0, verbose_name="Placar Time 1")
    nome_time2 = models.CharField(max_length=100, blank= False, verbose_name="Time 2")
    placar_time2 = models.IntegerField(default=0, verbose_name="Placar Time 2")
    partida_encerrada = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nome_time1 + " X " + self.nome_time2

    def encerrar_partida(self, placar_time1, placar_time2):
        if not self.partida_encerrada:
            self.placar_time1 = placar_time1
            self.placar_time2 = placar_time2
            self.verificar_ganhadores()
            self.partida_encerrada = True
            self.save()
        else:
            raise ValidationError(_('Partida já encerrada'), code='invalid')
    
    def verificar_ganhadores(self):
        ganhadores = []
        apostas = Aposta.objects.filter(partida__id_partida=self.id_partida)
        montante_apostas = 0
        for aposta in apostas:
            if aposta.placar_time1 == int(self.placar_time1) and aposta.placar_time2 == int(self.placar_time2):
                ganhadores.append(aposta.usuario)
            montante_apostas += aposta.valor_apostado

        if len(ganhadores) == 0:
            if self.placar_time1 > self.placar_time2:
                resultado = 1
            else:
                resultado = 2

            for aposta in apostas:
                if resultado == 0:
                    if aposta.placar_time1 == aposta.placar_time2:
                        ganhadores.append(aposta.usuario)
                elif resultado == 1:
                    if aposta.placar_time1 > aposta.placar_time2:
                        ganhadores.append(aposta.usuario)
                elif resultado == 2:
                    if aposta.placar_time1 < aposta.placar_time2:
                        ganhadores.append(aposta.usuario)
        if len(ganhadores) > 0:
            self.distribuir_premio(ganhadores, montante_apostas)
        else:
            self.devolver_saldo(apostas)

    def distribuir_premio(self, ganhadores, montante_apostas):
        premio_individual = montante_apostas / len(ganhadores)
        for ganhador in ganhadores:
            ganhador.receber_premiacao(premio_individual)

    
    def devolver_saldo(self, apostas):
        for aposta in apostas:
            aposta.usuario.devolver_valor()

    def __str__(self):
        return str(self.id_partida)
    
class Aposta(models.Model):
    id_aposta = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null= False)
    placar_time1 = models.IntegerField(default=0)
    placar_time2 = models.IntegerField(default=0)
    valor_apostado = MoneyField(max_digits=10,decimal_places=2,default_currency='BRL')
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE, null= False)

    def apostar(self, placar_time1, placar_time2, partida, usuario):
        if(usuario.saldo_player >= Money(amount='5', currency='BRL')):
            self.valor_apostado = Money(amount='5', currency='BRL')
            self.placar_time1 = placar_time1
            self.placar_time2 = placar_time2
            self.usuario = usuario
            self.partida = partida
            self.usuario.diminuir_saldo()
            self.save()
        else:
            raise ValidationError(_('Saldo Insuficiente'), code='invalid')

    def __str__(self):
        return str(self.id_aposta)
