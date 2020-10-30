from django.urls import path
from .views import *
app_name = 'console'
urlpatterns = [
    path('konsol/', console, name='console'),
]