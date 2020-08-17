from django.urls import path
from .views import *

app_name = 'info'
urlpatterns = [
    path('arkadaki-deha/', mastermind, name='mastermind'),
]