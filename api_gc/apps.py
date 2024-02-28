from django.apps import AppConfig


class ApiGcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_gc'
    def ready(self):
        import api_gc.signals
