from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import BookingForm, CustomUserCreationForm, ProfileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import UserProfile
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            # Здесь можно добавить обработку данных формы,
            # например, сохранить заказ или отправить уведомление
            return redirect('home')  # перенаправление после успешной обработки
    else:
        booking_form = BookingForm()
    return render(request, 'index.html', {'booking_form': booking_form})

def rooms(request):
    return render(request, 'rooms.html')

def restaurant(request):
    return render(request, 'restaurant.html')

def fitness(request):
    return render(request, 'fitness.html')

def events(request):
    return render(request, 'events.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Создание объекта User; профиль будет создан через сигнал
            login(request, user)  # Автоматический вход
            return redirect('account')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'profile_form': form})


def login_view(request):
    if request.method == 'POST':
        auth_form = AuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            user = auth_form.get_user()
            login(request, user)
            return redirect('account')
    else:
        auth_form = AuthenticationForm()
    return render(request, 'login.html', {'profile_form': auth_form})


@login_required
def account(request):
    # Получаем профиль пользователя или создаём его, если не существует
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Инициализируем формы: для редактирования профиля и для работы с бронированием.
    profile_form = ProfileForm(instance=profile)
    booking_form = BookingForm()  # Измените при необходимости для предзаполнения данных
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'profile':
            profile_form = ProfileForm(request.POST, instance=profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('account')
        elif form_type == 'booking':
            booking_form = BookingForm(request.POST)
            if booking_form.is_valid():
                booking_form.save()
                return redirect('account')
                
    context = {
        'profile_form': profile_form,
        'booking_form': booking_form,
        'name': profile.name if profile.name else request.user.username,
    }
    return render(request, 'account.html', context)


@login_required
def usersettings(request):
    # Получаем профиль пользователя или создаём его, если не существует
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    # Для отладки: выводим данные профиля (используем profile.name, а не profile.username)
    print("Профиль:", profile.name, profile.phone, profile.email)
    
    if request.method == 'POST' and request.POST.get('form_type') == 'profile':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('usersettings')
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, 'usersettings.html', {'form': form})


def enter(request):
    if request.user.is_authenticated:
        return redirect('account')
    return render(request, 'enter.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('enter')