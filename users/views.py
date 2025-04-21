from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from .models import Despesa
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        login = request.POST.get('login')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Senha e confirmar senha devem ser iguais.')
            return redirect('/users/register/')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve ter 6 ou mais caracteres.')
            return redirect('/users/register/')
        
        users = User.objects.filter(username=login)
        if users.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse login.')
            return redirect('/users/register/')
        
        emails = User.objects.filter(email=email)
        if emails.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse e-mail.')
            return redirect('/users/register/')

        User.objects.create_user(
            first_name=nome,
            email=email,
            username=login,
            password=senha
        )
        return redirect('/users/login/')
    
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        login = request.POST.get('login')
        senha = request.POST.get('senha')

        user = authenticate(request, username=login, password=senha)

        if user:
            auth.login(request, user)
            return redirect('/users/index/')
        
        messages.add_message(request, constants.ERROR, 'Login ou senha inválidos.')
        return redirect('login')

@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def contasPagar(request):
    despesas = Despesa.objects.filter(usuario=request.user)
    return render(request, 'contasPagar.html', {'despesas': despesas})

@login_required
def cadastrarDespesa(request):
    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        favorecido = request.POST.get('favorecido')
        valor = request.POST.get('valor')
        dataVencimento = request.POST.get('dataVencimento')  
        categoria = request.POST.get('categoria')

        Despesa.objects.create(
            descricao=descricao,
            favorecido=favorecido,
            valor=valor,
            dataVencimento=dataVencimento,
            categoria=categoria,
            usuario=request.user
        )

        messages.add_message(request, constants.SUCCESS, 'Despesa adicionada com sucesso.')
        return redirect('contasPagar')
    else:
        return render(request, 'cadastrarDespesa.html')

@login_required
def editarDespesa(request, id):
    despesa = Despesa.objects.get(id=id, usuario=request.user)

    if request.method == 'GET':
        return render(request, 'editarDespesa.html', {'despesa': despesa})
    elif request.method == 'POST':
        despesa.descricao = request.POST.get('descricao')
        despesa.favorecido = request.POST.get('favorecido')
        despesa.valor = request.POST.get('valor')
        despesa.dataVencimento = request.POST.get('dataVencimento')
        despesa.categoria = request.POST.get('categoria')
        despesa.save()

        messages.add_message(request, constants.SUCCESS, 'Despesa editada com sucesso.')
        return redirect('contasPagar')

@login_required
def excluirDespesa(request, id):
    despesa = Despesa.objects.filter(id=id, usuario=request.user).first()

    if despesa:
        despesa.delete()
        messages.add_message(request, constants.SUCCESS, 'Despesa excluída com sucesso.')

    return redirect('contasPagar')