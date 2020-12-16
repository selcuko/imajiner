from .models import Shadow
from django.contrib.auth import login
import hashlib

class ShadowMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.method == 'GET' and 0:
            shadow = self.is_shadow(request)
            if shadow is not None:
                login(request, shadow.user)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    
    def is_shadow(self, request):
        if request.user.is_authenticated:
            return None

        return Shadow.authenticate(request)
