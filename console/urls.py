from django.urls import path
from .views import *

app_name = 'console'

urlpatterns = [
    path('konsol/', Overview.as_view(), name='console'),
    path('konsol/ben/', Profile.as_view(), name='profile'),
    path('konsol/hikayeler/', Narratives.as_view(), name='narratives'),
    path('konsol/hikayeler/<uuid:uuid>/', Narratives.as_view(), name='narrative'),
    path('konsol/seriler/', Series.as_view(), name='series'),
    path('konsol/seriler/<uuid:uuid>', Series.as_view(), name='serie'),
]