from django.urls import path
from django.utils.translation import gettext_lazy as _
from .views import *

app_name = 'identity'
urlpatterns = [
    path(_('author/<str:username>/') , author_view, name='author'),
]