from django.apps import AppConfig


class ShashopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shashop'
    verbose_name = 'SHA-Lavka'

    def ready(self):
        import shashop.signals