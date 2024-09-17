from django.apps import AppConfig

class BrokerdataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'brokerdata'

    def ready(self):
        from .mqtt_client import start_mqtt_client  # Import here to avoid circular imports
        start_mqtt_client()
