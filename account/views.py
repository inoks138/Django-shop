from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from .forms import AccountRegisterForm, AccountLoginForm


def register(request):
    if request.method == 'POST':
        form = AccountRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = AccountRegisterForm()
    return render(request, 'account/register.html', {"form": form})


def account_login(request):
    if request.method == 'POST':
        form = AccountLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AccountLoginForm()
    return render(request, 'account/login.html', {"form": form})


def account_logout(request):
    logout(request)
    return redirect('login')
