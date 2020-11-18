from django.urls import path
from django.views.generic import RedirectView
from .views import *
from django.utils.translation import gettext_lazy as _

app_name = 'notebook'
urlpatterns = [
    path('', NarrativeList.as_view(), name='list'),

    path(_('write/'), NarrativeFolder.as_view(), name='folder'),
    path(_('write/new/'), NarrativeWrite.as_view(), name='write'),
    path(_('write/<uuid:uuid>/'), NarrativeWrite.as_view(), name='sketch'),

    path('<slug:slug>/', NarrativeDetail.as_view(), name='detail'),
]