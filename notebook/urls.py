from django.urls import path
from django.views.generic import RedirectView
from .views import *

app_name = 'notebook'
urlpatterns = [
    path('hikaye/', NarrativeList.as_view(), name='list'),
    path('hikayeler/', RedirectView.as_view(pattern_name='notebook:list', permanent=True)),

    path('hikaye/yaz/', NarrativeFolder.as_view(), name='folder'),
    path('hikaye/yaz/yeni/', NarrativeWrite.as_view(), name='write'),
    path('hikaye/yaz/<uuid:uuid>/', NarrativeWrite.as_view(), name='sketch'),

    path('hikaye/<slug:slug>/', NarrativeDetail.as_view(), name='detail'),

    path('ses/', SoundUpload.as_view(), name='upload'),
]