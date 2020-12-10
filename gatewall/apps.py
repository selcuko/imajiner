from django.apps import AppConfig


class GatewallConfig(AppConfig):
    name = 'gatewall'

    def ready(self):
        from django.urls import reverse
        from django.conf import settings
        settings.LOGIN_URL = f"{reverse('gatewall:auth')}?informative"
