from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('/bolao/aposta/', views.realizar_aposta, name='realizar_aposta'),
    path('accounts/signup',views.signup, name='signup'),
    path('partidas/criar',views.cadastrarPartida, name='cadastrarPartida'),
    path('accounts/list',views.list_Users, name='listaUsuarios'),
    path('partidas/list',views.list_Partidas, name='listaPartidas'),
    url(r'^partidas/encerra_Partida/(?P<pk>\d+)/(?P<p1>\d+)/(?P<p2>\d+)/$',views.encerra_Partida, name='encerraPartida'),
    url(r'^accounts/adiciona_Saldo/(?P<pk>\d+)/(?P<valor>\d+\.\d{2})/$',views.adicionarSaldo, name='adicionarSaldo')

    # path('', views.index),
]