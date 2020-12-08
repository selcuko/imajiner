from django.contrib import admin
from django.contrib.sessions.models import Session
from django.utils.safestring import SafeString
from .models import LoggedInUser, Profile, Shadow


admin.site.register(LoggedInUser)
admin.site.register(Session)
admin.site.register(Shadow)
admin.site.register(Profile)