from django.urls import path

from .views import Home, Infinite

app_name = 'explore'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('inf', Infinite.as_view(), name='inf')
]