from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView

from .views import *

app_name = 'notebook'
urlpatterns = [
    path('', List.as_view(), name='list'),
    path(_('write/'), Folder.as_view(), name='folder'),
    path(_('write/new/'), FreshWrite.as_view(), name='write'),
    path(_('write/<uuid:uuid>/'), ContinueSketch.as_view(), name='sketch'),
    path(_('translate/<uuid:uuid>/'), AddTranslation.as_view(),
         kwargs={'redirect': False}, name='translate'),
    path(_('retranslate/<uuid:uuid>/'), AddTranslation.as_view(),
         kwargs={'redirect': True}, name='retranslate'),
    path('<slug:slug>/', Detail.as_view(), name='detail'),
]
