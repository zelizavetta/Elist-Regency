# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name or self.user.username
    

class Room(models.Model):
    """Отдельный номер в отеле."""
    number = models.CharField("Номер", max_length=10, unique=True)
    room_type = models.CharField("Тип номера", max_length=50,
                                 choices=[
                                     ("comfort", "Комфорт"),
                                     ("comfort_plus", "Комфорт+"),
                                     ("apartment", "Апартаменты"),
                                 ])
    price = models.DecimalField("Цена за ночь", max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ["number"]

    def __str__(self):
        return f"Номер {self.number} ({self.get_room_type_display()})"


class Booking(models.Model):
    """Бронь целиком (диапазон дат)."""
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="bookings",
        null=True,    # теперь поле может быть пустым
        blank=True
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="bookings", verbose_name="Пользователь")
    check_in = models.DateField("Дата заезда")
    check_out = models.DateField("Дата выезда")
    guests = models.PositiveIntegerField("Взрослые", default=1)
    children = models.PositiveIntegerField("Дети", default=0)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        ordering = ["-created_at"]
        # предотвращаем накладку по одному и тому же номеру в один и тот же день
        constraints = [
            models.UniqueConstraint(
                fields=["room", "check_in", "check_out"],
                name="unique_room_booking"
            )
        ]

    def __str__(self):
        return (f"Бронь №{self.id}: {self.room.number} "
                f"{self.check_in}–{self.check_out} ({self.user.username})")


class RoomBookedDate(models.Model):
    """
    Опционально: если нужно хранить каждую дату в отдельной записи,
    чтобы быстро фильтровать занятые дни без обхода диапазона.
    """
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="booked_dates",
        null=True,    # теперь поле может быть пустым
        blank=True
    )

    date = models.DateField("Занятая дата")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE,
                                related_name="dates", verbose_name="Бронирование")

    class Meta:
        verbose_name = "Занятая дата номера"
        verbose_name_plural = "Занятые даты номеров"
        unique_together = [["room", "date"]]
        ordering = ["date"]

    def __str__(self):
        return f"{self.room.number} занято {self.date}"


class Restaurant(models.Model):
    RESTAURANT = 'restaurant'
    BAR        = 'bar'
    TYPE_CHOICES = [
        (RESTAURANT, 'Ресторан'),
        (BAR,        'Бар'),
    ]
    name = models.CharField('Название', max_length=100)
    type = models.CharField('Тип', max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return f'{self.get_type_display()}: {self.name}'

class Dish(models.Model):
    restaurant  = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='dishes')
    name        = models.CharField('Блюдо', max_length=100)
    description = models.TextField('Описание', blank=True)
    price       = models.DecimalField('Цена', max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина {self.user.username}'

    def total(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    dish     = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'dish')

    def __str__(self):
        return f'{self.dish.name} × {self.quantity}'

    def total_price(self):
        return self.dish.price * self.quantity
