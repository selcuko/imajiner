from django.urls import path
from .views import *

app_name = 'console'

urlpatterns = [
    path('konsol/', Overview.as_view(), name='overview'),
    path('konsol/ben/', Profile.as_view(), name='profile'),
    path('konsol/erisim/', Access.as_view(), name='access'),
    path('konsol/hikayeler/', Narratives.as_view(), name='publications'),
    path('konsol/hikayeler/<uuid:uuid>/', Narrative.as_view(), name='narrative'),
    path('konsol/taslak/', Sketches.as_view(), name='sketches'),
    path('konsol/taslak/<uuid:uuid>/', Sketch.as_view(), name='sketch'),
    path('konsol/seriler/', Series.as_view(), name='series'),
    path('konsol/seriler/<uuid:uuid>', Serie.as_view(), name='serie'),
    path('konsol/medya/', Medium.as_view(), name='medium'),
    path('konsol/medya/<uuid:uuid>/', Media.as_view(), name='media'),
]