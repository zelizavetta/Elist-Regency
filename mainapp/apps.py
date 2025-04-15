# apps.py
from django.apps import AppConfig

class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'

    def ready(self):
        # Импортируем модуль сигналов, чтобы они зарегистрировались
        import mainapp.signals
