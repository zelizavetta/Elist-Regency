# models.py
from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.conf import settings
from django.core.files.storage import FileSystemStorage

dish_static_fs = FileSystemStorage(
    location=settings.DISH_STATIC_ROOT,
    base_url=settings.DISH_STATIC_URL,
)

room_static_fs = FileSystemStorage(
    location=settings.ROOM_STATIC_ROOT,
    base_url=settings.ROOM_STATIC_URL,
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name or self.user.username


class Room(models.Model):
    COMFORT      = "comfort"
    COMFORT_PLUS = "comfort_plus"
    APARTMENT    = "apartment"

    ROOM_TYPE_CHOICES = [
        (COMFORT,      "Комфорт"),
        (COMFORT_PLUS, "Комфорт+"),
        (APARTMENT,    "Апартаменты"),
    ]

    ROOM_DESCRIPTION_CHOICES = [
        (COMFORT,      "Уютный номер стандартного класса, оборудованный всеми\nнеобходимыми удобствами:\nсовременная мебель, телевизор, бесплатный Wi-Fi,\nмини-бар и кондиционер.\nПодходит для комфортного проживания по доступной цене."),
        (COMFORT_PLUS, "Улучшенная версия номера «Комфорт»\nс дополнительными деталями:\nболее стильный интерьер, расширенное пространство,\nулучшенные условия в ванной комнате\nи дополнительные сервисы (например,\nкруглосуточное обслуживание или мини-кухня).\nИдеален для гостей, ценящих немного больше уюта и удобств."),
        (APARTMENT,    "Просторные и функциональные номера\nс отдельнойгостиной и кухонной зоной,\nчто позволяетгостям чувствовать себя как дома.\nАпартаменты подходят для длительного проживания,\nсемей или гостей, нуждающихся в дополнительном\nпространстве и приватности."),
    ]

    number    = models.CharField("Номер", max_length=10, unique=True)
    room_type = models.CharField("Тип номера",
                                 max_length=50,
                                 choices=ROOM_TYPE_CHOICES)
    price     = models.DecimalField("Цена за ночь",
                                    max_digits=8, decimal_places=2)

    image = models.ImageField(
        'Фото номера',
        storage=room_static_fs,
        upload_to='',       
        blank=True,
        null=True
    )
    

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ["number"]

    def __str__(self):
        return f"Номер {self.number} ({self.get_room_type_display()})"
    
    @property
    def description(self):
        return dict(self.ROOM_DESCRIPTION_CHOICES).get(self.room_type, "")

    # # статическая мапа тип→путь
    # IMAGE_MAP = {
    #     COMFORT:      'img/room2.jpg',
    #     COMFORT_PLUS: 'img/room3.jpg',
    #     APARTMENT:    'img/room7.jpg',
    # }

    @property
    def image_url(self):
        """
        Возвращает полный URL к картинке.
        Если self.image пусто — возвращает статический URL дефолтной картинки.
        """
        if self.image and hasattr(self.image, 'url'):
            # .url уже учитывает storage.base_url + имя файла
            return self.image.url
        # подставляем свой дефолт из STATIC
        return static('img/rooms/default_room.jpg')


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
    RESTAURANT1 = 'restaurant1'
    RESTAURANT2 = 'restaurant2'
    BAR        = 'bar'
    NAME_CHOICES = [
        (RESTAURANT1, 'Ресторан: Вкусный Дом'),
        (RESTAURANT2, 'Ресторан: Гурме Хаус'),
        (BAR,        'Бар: Sky Lounge Bar'),
    ]

    DESCRIPTION_CHOICES = [
        (RESTAURANT1, 'Описание ресторана 1'),
        (RESTAURANT2, 'Описание ресторана 2'),
        (BAR,        'Описание бара'),
    ]

    name = models.CharField('Название ресторана', max_length=100, choices=NAME_CHOICES)

    @property
    def description(self):
        return dict(self.DESCRIPTION_CHOICES).get(self.name, "")

    # статическая мапа тип→путь
    IMAGE_MAP = {
        RESTAURANT1: 'img/restaurant2.jpg',
        RESTAURANT2: 'img/restaurant4.jpg',
        BAR: 'img/restaurant1.jpg',
    }

    @property
    def image_url(self):
        """
        Возвращаем статический путь в зависимости от room_type.
        Для использования в шаблоне как {{ room.image_url }}.
        """
        # static() оборачивает относительный путь в URL из STATIC_URL
        return static(self.IMAGE_MAP.get(self.name, 'img/default.jpg'))


    def __str__(self):
        return self.get_name_display()
    
    def __repr__(self):
        return self.get_name_display()

    
class Dish(models.Model):
    restaurant  = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='dishes', verbose_name="Ресторан")
    name        = models.CharField('Блюдо', max_length=100)
    description = models.TextField('Описание', blank=True)
    price       = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    image = models.ImageField(
        'Фото блюда',
        storage=dish_static_fs,
        upload_to='',       
        blank=True,
        null=True
    )

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return static('img/dishes/default_dish.jpg')


    def __str__(self):
        return self.name


class Cart(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    order_date = models.DateField("Дата доставки", null=True, blank=True)
    order_time = models.TimeField("Время доставки", null=True, blank=True)


    def __str__(self):
        return f'Корзина {self.user.username}'

    def total(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart     = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    dish     = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='cart_items',
        null=True,    
        blank=True    
    )
    order_date = models.DateField("Дата доставки", null=True, blank=True)
    order_time = models.TimeField("Время доставки", null=True, blank=True)

    class Meta:
        unique_together = ('cart', 'dish', 'booking')

    def __str__(self):
        return f'{self.dish.name} × {self.quantity}'

    def total_price(self):
        return self.dish.price * self.quantity

class Review(models.Model):
    STAR_CHOICES = [(i, f"{i} зв{'езда' if i==1 else 'ез'}") for i in range(1,6)]
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating     = models.IntegerField("Оценка", choices=STAR_CHOICES)
    text       = models.TextField("Текст отзыва")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.rating}/5"