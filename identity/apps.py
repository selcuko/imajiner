from django.apps import AppConfig

class IdentityConfig(AppConfig):
    name = 'identity'

    def ready(self):
        from django.contrib.auth.models import User, AnonymousUser
        from .methods import sessions, is_shadow, agent
        User.add_to_class('is_shadow', is_shadow)
        User.add_to_class('sessions', sessions)
        User.add_to_class('agent', agent)

