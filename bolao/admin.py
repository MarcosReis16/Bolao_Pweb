from django.contrib import admin
from .models import ( Usuario, Aposta, Partida, EncerrarPartida)
from .forms import (CustomUserAdmin, ApostarForm, CriarPartidaAdmin, EncerrarPartidaAdmin)

# Register your models here.
admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Partida, CriarPartidaAdmin)
admin.site.register(EncerrarPartida, EncerrarPartidaAdmin)
# admin.site.register(Aposta)
# admin.site.register(ApostarForm)

