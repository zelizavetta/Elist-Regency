from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import BookingForm, CustomUserCreationForm, ProfileForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import UserProfile, Booking, Room, RoomBookedDate, Restaurant, Dish, Cart, CartItem
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Q
from datetime import datetime, timedelta
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect


def index(request):
    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            check_in  = booking_form.cleaned_data['check_in']
            check_out = booking_form.cleaned_data['check_out']

            # 1) Найти броня, пересекающиеся с выбранным диапазоном
            overlapping = Booking.objects.filter(
                Q(check_in__lt=check_out) &
                Q(check_out__gt=check_in)
            ).values_list('room_id', flat=True)

            # 2) Все номера, не попавшие в overlapping
            available_rooms = Room.objects.exclude(id__in=overlapping)

            return render(request, 'available_rooms.html', {
                'rooms': available_rooms,
                'check_in': check_in,
                'check_out': check_out,
            })
    else:
        booking_form = BookingForm()

    # Для flatpickr собираем занятые даты всех номеров (если нужен календарь)
    booked_dates = []
    for b in Booking.objects.all():
        d = b.check_in
        while d <= b.check_out:
            booked_dates.append(d.strftime('%Y-%m-%d'))
            d += timedelta(days=1)
    booked_dates = sorted(set(booked_dates))

    return render(request, 'index.html', {
        'booking_form': booking_form,
        'booked_dates_json': json.dumps(booked_dates),
    })

@login_required
def find_rooms(request):
    if request.method != 'POST':
        return redirect('home')

    form = BookingForm(request.POST)
    if not form.is_valid():
        return render(request, 'booking.html', {'booking_form': form})

    check_in  = form.cleaned_data['check_in']
    check_out = form.cleaned_data['check_out']

    overlapping = Booking.objects.filter(
        check_in__lt=check_out,
        check_out__gt=check_in
    ).values_list('room_id', flat=True)

    available = Room.objects.exclude(id__in=overlapping)

    return render(request, 'find_rooms.html', {
        'rooms': available,
        'check_in': check_in,
        'check_out': check_out
    })

# views.py
@login_required
def book_room(request):
    if request.method != 'POST':
        return redirect('home')

    room = get_object_or_404(Room, pk=request.POST.get('room_id'))

    # Собираем форму сразу из POST, включая guests и children
    form = BookingForm(request.POST)
    if not form.is_valid():
        # Здесь можно перенаправить назад с ошибками
        return redirect('find_rooms')

    booking = form.save(commit=False)
    booking.user = request.user
    booking.room = room
    booking.save()

    # Обновляем RoomBookedDate
    d = booking.check_in
    while d <= booking.check_out:
        RoomBookedDate.objects.create(room=room, date=d, booking=booking)
        d += timedelta(days=1)

    return redirect('account')


def room_list(request):
    """
    Список всех комнат.
    """
    rooms = Room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})

@login_required
def room_detail(request, pk):
    """
    Детальная страница конкретного номера + форма бронирования,
    где занятые даты отключены в календаре.
    """
    room = get_object_or_404(Room, pk=pk)

    # 1) Получаем все даты, которые уже заняты для этого номера
    dates_qs = RoomBookedDate.objects.filter(room=room).values_list('date', flat=True)
    booked_dates = [d.strftime('%Y-%m-%d') for d in dates_qs]

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # 2) Сохраняем новое бронирование
            booking = form.save(commit=False)
            booking.user = request.user
            booking.room = room
            booking.save()

            # 3) Разбиваем диапазон check_in–check_out на одиночные даты
            d = booking.check_in
            while d <= booking.check_out:
                RoomBookedDate.objects.create(room=room, date=d, booking=booking)
                d += timedelta(days=1)

            return redirect('booking_success')  # или на какую‑нибудь "Спасибо" страницу
    else:
        form = BookingForm()

    return render(request, 'room_detail.html', {
        'room': room,
        'form': form,
        'booked_dates_json': json.dumps(booked_dates),
    })

def rooms(request):
    # ваше представление, например:
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms': rooms})


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
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    profile_form = ProfileForm(instance=profile)
    booking_form = BookingForm()

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
                booking = booking_form.save(commit=False)
                booking.user = request.user
                # если надо, привяжите и room, либо обрабатывайте как у вас
                booking.save()
                return redirect('account')

    # Существующие брони текущего пользователя
    user_bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    # Опционально: если вам нужен booked_dates_json для календаря на этой странице
    booked_dates = []
    for b in Booking.objects.all():
        d = b.check_in
        while d <= b.check_out:
            booked_dates.append(d.strftime('%Y-%m-%d'))
            d += timedelta(days=1)
    booked_dates = sorted(set(booked_dates))

    return render(request, 'account.html', {
        'profile_form': profile_form,
        'booking_form': booking_form,
        'name': profile.name or request.user.username,
        'bookings': user_bookings,
        'booked_dates_json': json.dumps(booked_dates),
    })

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

def restaurants(request):
    qs = Restaurant.objects.all()
    return render(request, 'restaurants.html', {'restaurants': qs})

def restaurant_detail(request, pk):
    r = get_object_or_404(Restaurant, pk=pk)
    return render(request, 'restaurant.html', {
        'restaurant': r,
        'dishes': r.dishes.all()
    })

@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {
        'cart': cart,
        'items': cart.items.select_related('dish'),
        'total': cart.total(),
    })

@login_required
@require_POST
def cart_add(request):
    dish_id  = request.POST.get('dish_id')
    quantity = int(request.POST.get('quantity', 1))
    dish     = get_object_or_404(Dish, pk=dish_id)
    cart, _  = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, dish=dish)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    # куда редиректим — сначала смотрим hidden next, затем Referer, иначе на главную
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(next_url)

@login_required
@require_POST
def cart_remove(request):
    item_id = request.POST.get('item_id')
    item    = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_detail')