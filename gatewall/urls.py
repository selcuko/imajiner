from django.urls import path

from .views import LoginViews, Auth

app_name = 'gatewall'
urlpatterns = [
    path('ben-kimim/', Auth.as_view(), name='auth')
]