from django.apps import AppConfig


class DatateknisConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.datateknis"
    label = "datateknis"

    def ready(self):
        import apps.datateknis.singals
