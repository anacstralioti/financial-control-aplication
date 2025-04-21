from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('contasPagar/', views.contasPagar, name='contasPagar'),
    path('cadastrarDespesa/', views.cadastrarDespesa, name='cadastrarDespesa'),
    path('editarDespesa/<int:id>/', views.editarDespesa, name='editarDespesa'),
    path('excluirDespesa/<int:id>/', views.excluirDespesa, name='excluirDespesa'),
]
