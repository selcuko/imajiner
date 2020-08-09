from django.urls import path
from .views import *

app_name = 'identity'
urlpatterns = [
    path('yazar/<str:username>/', author_view, name='author'),
]