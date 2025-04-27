from django.urls import path
from . import views


urlpatterns = [
    path("", views.manager_dashboard, name='manager_dashboard'),
    path('room/<int:pk>/edit/', views.manager_edit_room, name='manager_edit_room'),
    path('stats/', views.statistics_view, name='manager_stats'),
    path('dishes/',           views.DishListView.as_view(),   name='manager_dish_list'),
    path('dishes/add/',       views.DishCreateView.as_view(), name='manager_dish_add'),
    path('dishes/<int:pk>/edit/',   views.DishUpdateView.as_view(), name='manager_dish_edit'),
    path('dishes/<int:pk>/delete/', views.DishDeleteView.as_view(), name='manager_dish_delete'),
    path('rooms/',             views.RoomListView.as_view(),   name='manager_room_list'),
    path('rooms/add/',         views.RoomCreateView.as_view(), name='manager_room_add'),
    path('rooms/<int:pk>/edit/',   views.RoomUpdateView.as_view(), name='manager_room_edit'),
    path('rooms/<int:pk>/delete/', views.RoomDeleteView.as_view(), name='manager_room_delete'),
]
