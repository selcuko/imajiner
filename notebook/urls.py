from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView

from .views import *

app_name = 'notebook'
urlpatterns = [
    path('', List.as_view(), name='list'),
    path(_('write/'), Folder.as_view(), name='folder'),
    path(_('write/new/'), Write.as_view(), name='write'),
    path(_('write/<uuid:uuid>/'), Write.as_view(), name='sketch'),
    path(_('translate/<uuid:uuid>/'), AddTranslation.as_view(), name='translate'),
    path('<slug:slug>/', Detail.as_view(), name='detail'),
]
