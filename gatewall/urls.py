from django.urls import path
from django.utils.translation import gettext_lazy as _
from .views import *

app_name = 'gatewall'
urlpatterns = [
    path(_('authorization/') , Auth.as_view(), name='auth'),
    path(_('farewell/'), Logout.as_view(), name='logout'),
]