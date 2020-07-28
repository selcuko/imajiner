from django.urls import path

from .views import LoginViews

app_name = 'gatewall'
urlpatterns = [
    path('ben-kimim/', LoginViews.Login.as_view(), name='login'),
]