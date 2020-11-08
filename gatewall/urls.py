from django.urls import path

from .views import *

app_name = 'gatewall'
urlpatterns = [
    path('ben-kimim/', Auth.as_view(), name='auth'),
    path('terk-et/', Logout.as_view(), name='logout'),
]