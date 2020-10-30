from django.urls import path
from .views import *
app_name = 'console'
urlpatterns = [
    path('konsol/', Console.as_view(), name='console'),
]