from django.urls import path
from .views import *

app_name = 'cnc'
urlpatterns = [
    path('komuta/', CommandAndControl.as_view(), name='panel'),
]