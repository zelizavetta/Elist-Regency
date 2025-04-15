# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Создаем профиль с начальными значениями
        UserProfile.objects.get_or_create(
            user=instance,
            name=instance.username,    # или другое значение по умолчанию
            email=instance.email       # если email введен при регистрации
        )
