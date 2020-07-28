from django.apps import AppConfig

class IdentityConfig(AppConfig):
    name = 'identity'

    def ready(self):
        from django.contrib.auth.models import User, AnonymousUser

        @property
        def is_shadow(self):
            try:
                is_shadow = self.shadow
                return self.shadow.active
            except:
                return False

        User.add_to_class('is_shadow', is_shadow)

