from django.urls import path
from . import views

urlpatterns = [
    path('/bolao/aposta/', views.realizar_aposta, name='realizar_aposta'),
    path('accounts/signup',views.signup, name='signup')
    # path('', views.index),
]