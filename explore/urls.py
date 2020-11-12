from django.urls import path

from .views import *

app_name = 'explore'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('inf', Infinite.as_view(), name='inf'),
    path('red', red),
]