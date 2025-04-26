from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path('restaurants/',           views.restaurants,       name='restaurants'),
    path('restaurants/<int:pk>/',  views.restaurant_detail, name='restaurant_detail'),
    path('cart/add/',              views.cart_add,          name='cart_add'),
    path('cart/remove/',           views.cart_remove,       name='cart_remove'),
    path('cart/',                  views.cart_detail,       name='cart_detail'),
    path("fitness/", views.fitness, name="fitness"),
    path("events/", views.events, name="events"),
    path('gallery/', views.gallery, name='gallery'),
    path("account/", views.account, name="account"),
    path("usersettings/", views.usersettings, name="usersettings"),
    path("enter/", views.enter, name="enter"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('find_rooms/', views.find_rooms, name='find_rooms'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
    path('book_room/', views.book_room, name='book_room'),
    path('rooms/', views.rooms, name='rooms'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
