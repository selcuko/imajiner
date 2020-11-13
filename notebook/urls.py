from django.urls import path
from django.views.generic import RedirectView
from .views import *

app_name = 'notebook'
urlpatterns = [
    path('', NarrativeList.as_view(), name='list'),

    path('yaz/', NarrativeFolder.as_view(), name='folder'),
    path('yaz/yeni/', NarrativeWrite.as_view(), name='write'),
    path('yaz/<uuid:uuid>/', NarrativeWrite.as_view(), name='sketch'),

    path('<slug:slug>/', NarrativeDetail.as_view(), name='detail'),
]