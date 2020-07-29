from django.urls import path

from .views import NarrativeViews

app_name = 'notebook'
urlpatterns = [
    path('hikayeler/', NarrativeViews.List.as_view(), name='list'),
    path('hikaye/yaz/', NarrativeViews.Write.as_view(), name='write'),
    path('hikaye/<slug:slug>/', NarrativeViews.Detail.as_view(), name='detail'),
]