from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("rooms/", views.rooms, name="rooms"),
    path("restaurant/", views.restaurant, name="restaurant"),
    path("fitness/", views.fitness, name="fitness"),
    path("events/", views.events, name="events"),
    path("account/", views.account, name="account"),
    path("usersettings/", views.usersettings, name="usersettings"),
    path("enter/", views.enter, name="enter"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
