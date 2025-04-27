from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),

    # Бронирование комнат
    path("find_rooms/", views.find_rooms, name="find_rooms"),
    path("rooms/", views.rooms, name="rooms"),
    path("rooms/<int:pk>/", views.room_detail, name="room_detail"),
    path("book_room/", views.book_room, name="book_room"),
    path("booking/cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),

    # Дополнительные услуги
    path("cleaning/<int:booking_pk>/", views.cleaning, name="cleaning"),

    path("menu_restaurants/", views.menu_restaurants, name="menu_restaurants"),
    path("menu_restaurants/<int:pk>/", views.menu_restaurant_detail, name="menu_restaurant_detail"),
    path("restaurants/<int:booking_pk>/", views.restaurants, name="restaurants"),
    path("restaurants/<int:booking_pk>/restaurant/<int:rest_pk>/", views.restaurant_detail, name="restaurant_detail"),

    # Корзина и оформление заказа
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/", views.cart_add, name="cart_add"),
    path("cart/remove/", views.cart_remove, name="cart_remove"),
    path("cart/order/", views.order_restaurant, name="order_restaurant"),

    # Пользовательский аккаунт
    path("account/", views.account, name="account"),
    path("usersettings/", views.usersettings, name="usersettings"),

    # Аутентификация
    path("enter/", views.enter, name="enter"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Прочие страницы
    path("fitness/", views.fitness, name="fitness"),
    path("events/", views.events, name="events"),
    path("gallery/", views.gallery, name="gallery"),
    path("review/", views.leave_review, name="leave_review"),
    


]
