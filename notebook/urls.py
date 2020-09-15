from django.urls import path
from django.views.generic import RedirectView
from .views import NarrativeView, NarrativeFactory, SoundUpload

app_name = 'notebook'
urlpatterns = [
    path('hikaye/', NarrativeView.List.as_view(), name='list'),
    path('hikayeler/', RedirectView.as_view(pattern_name='notebook:list', permanent=True)),

    path('hikaye/yaz/', NarrativeFactory.Write.as_view(), name='write'),
    path('hikaye/yaz/yeni/', NarrativeFactory.New.as_view(), name='new'),
    path('hikaye/yaz/<slug:slug>/', NarrativeFactory.Sketch.as_view(), name='sketch'),

    path('hikaye/<slug:slug>/', NarrativeView.Detail.as_view(), name='detail'),

    path('ses/', SoundUpload.as_view(), name='upload'),
]