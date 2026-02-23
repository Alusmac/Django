from django.apps import AppConfig


class FormsUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'forms_user'

    def ready(self):
        pass