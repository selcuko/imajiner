from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import LoggedInUser


admin.site.register(LoggedInUser)
admin.site.register(Session)