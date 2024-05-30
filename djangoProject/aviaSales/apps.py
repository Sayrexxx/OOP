from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aviaSales'

    def ready(self):
        import aviaSales.signals
