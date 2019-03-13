from django.apps import AppConfig


class RestserviceConfig(AppConfig):
    name = 'restservice'
    
    def ready(self):
        import restservice.signals