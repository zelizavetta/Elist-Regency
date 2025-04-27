from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models.functions import ExtractYear
import calendar
from datetime import datetime, date
from django.db.models import Avg, Count
from mainapp.models import Booking, Room, UserProfile, Restaurant, Review, Dish
from .forms import DishForm, RoomForm


@staff_member_required
def manager_dashboard(request):
    qs = Booking.objects.select_related('user','room').order_by('-created_at')

    years = (
        Booking.objects
               .annotate(year=ExtractYear('check_in'))
               .values_list('year', flat=True)
               .distinct()
               .order_by('-year')
    )
    # месяцы 1–12
    months = [(i, calendar.month_name[i]) for i in range(1,13)]

    # читаем GET-параметры
    sel_year  = request.GET.get('year')
    sel_month = request.GET.get('month')
    if sel_year:
        qs = qs.filter(check_in__year=sel_year)
    if sel_month:
        qs = qs.filter(check_in__month=sel_month)

    context = {
        'rooms': Room.objects.all(),
        'profiles': UserProfile.objects.select_related('user'),
        'restaurants': Restaurant.objects.prefetch_related('dishes').all(),
        'bookings':    qs,
        'years':       years,
        'months':      months,
        'sel_year':    sel_year,
        'sel_month':   sel_month,
    }
    agg = Review.objects.aggregate(
        avg_rating=Avg('rating'),
        total=Count('id'),
    )
    context.update({
        'reviews': Review.objects.select_related('user'),
        'avg_rating': agg['avg_rating'] or 0,
        'reviews_count': agg['total'],
    })
    return render(request, 'manager/dashboard.html', context)

@login_required
@staff_member_required
@require_POST
def manager_edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    # Читаем price из POST и сохраняем
    new_price = request.POST.get('price')
    try:
        room.price = float(new_price)
        room.save()
    except (TypeError, ValueError):
        # можно передать ошибку в сессию или логи
        pass
    return redirect('manager_dashboard')

@staff_member_required
def statistics_view(request):
    # анализируем текущий год
    year = date.today().year

    # инициализируем словарь: для каждого месяца — ночей и выручки = 0
    stats = {m: {'nights': 0, 'revenue': 0} for m in range(1, 13)}

    # выбираем все брони с датой заезда в этом году
    bookings = Booking.objects.filter(check_in__year=year)

    for b in bookings:
        month = b.check_in.month
        # сколько ночей
        nights = (b.check_out - b.check_in).days
        stats[month]['nights']  += nights
        stats[month]['revenue'] += nights * b.room.price

    # превращаем в упорядоченный список для шаблона
    stats_list = []
    for m in range(1, 13):
        stats_list.append({
            'month':   calendar.month_name[m],       # Январь, Февраль…
            'nights':  stats[m]['nights'],
            'revenue': stats[m]['revenue'],
        })

    # общая выручка за год
    total_revenue = sum(item['revenue'] for item in stats_list)

    return render(request, 'manager/statistics.html', {
        'year':          year,
        'stats_list':    stats_list,
        'total_revenue': total_revenue,
    })

@method_decorator([login_required, staff_member_required], name='dispatch')
class DishListView(ListView):
    model = Dish
    template_name = 'manager/dish_list.html'
    context_object_name = 'dishes'

@method_decorator([login_required, staff_member_required], name='dispatch')
class DishCreateView(CreateView):
    model = Dish
    form_class = DishForm
    template_name = 'manager/dish_form.html'
    success_url = reverse_lazy('manager_dish_list')

@method_decorator([login_required, staff_member_required], name='dispatch')
class DishUpdateView(UpdateView):
    model = Dish
    form_class = DishForm
    template_name = 'manager/dish_form.html'
    success_url = reverse_lazy('manager_dish_list')

@method_decorator([login_required, staff_member_required], name='dispatch')
class DishDeleteView(DeleteView):
    model = Dish
    template_name = 'manager/dish_confirm_delete.html'
    success_url = reverse_lazy('manager_dish_list')

decorators = [login_required, staff_member_required]

@method_decorator(decorators, name='dispatch')
class RoomListView(ListView):
    model = Room
    template_name = 'manager/room_list.html'
    context_object_name = 'rooms'

@method_decorator(decorators, name='dispatch')
class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'manager/room_form.html'
    success_url = reverse_lazy('manager_room_list')

@method_decorator(decorators, name='dispatch')
class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'manager/room_form.html'
    success_url = reverse_lazy('manager_room_list')

@method_decorator(decorators, name='dispatch')
class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'manager/room_confirm_delete.html'
    success_url = reverse_lazy('manager_room_list')