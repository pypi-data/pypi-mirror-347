
from django.apps import AppConfig
from .utils import add_dynamic_property, load_language


class SepidarApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_base_django'

    def ready(self):
        add_dynamic_property()
        from . import functions
        load_language()
