from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BookingForm, UserForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def index(request):
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            # Здесь можно добавить обработку данных формы,
            # например, сохранить заказ, отправить уведомление и т.д.
            return redirect('home')  # перенаправление после успешной обработки
    else:
        booking_form = BookingForm()
    return render(request, 'index.html', {'form': booking_form})

def rooms(request):
    return render(request, 'rooms.html')

def restaurant(request):
    return render(request, 'restaurant.html')

def fitness(request):
    return render(request, 'fitness.html')

def events(request):
    return render(request, 'events.html')

def usersettings(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Здесь можно добавить обработку данных формы,
            # например, сохранить заказ, отправить уведомление и т.д.
            print("OK")
    else:
        form = UserForm()
    return render(request, 'usersettings.html', {'form': form})

def account(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Здесь можно добавить обработку данных формы,
            # например, сохранить заказ, отправить уведомление и т.д.
            print("OK")
    else:
        form = BookingForm()
    return render(request, 'account.html', {'form': form})

def enter(request):
    if request.user.is_authenticated:
        return redirect('account')
    return render(request, 'enter.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('enter')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()          # Создаём пользователя
            login(request, user)        # Автоматически логиним нового пользователя
            return render(request, 'account.html', {'name': user.username})     # Перенаправляем на главную страницу
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'account.html', {'name': user.username})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

