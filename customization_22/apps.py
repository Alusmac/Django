from django.apps import AppConfig


class Customization22Config(AppConfig):
    """Configuration for the 'customization_22'  app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customization_22'

    def ready(self) -> None:
        """Import signals when the app is ready to ensure they are registered
        """
        import customization_22.signals
