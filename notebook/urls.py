from django.urls import path

from .views import NarrativeView, NarrativeFactory

app_name = 'notebook'
urlpatterns = [
    path('hikayeler/', NarrativeView.List.as_view(), name='list'),

    path('hikaye/yaz/', NarrativeFactory.Write.as_view(), name='write'),
    path('hikaye/yaz/yeni/', NarrativeFactory.New.as_view(), name='new'),
    #path('hikaye/yaz/<slug:slug>/', NarrativeFactory.Sketch.as_view, name='sketch'),

    path('hikaye/<slug:slug>/', NarrativeView.Detail.as_view(), name='detail'),
]