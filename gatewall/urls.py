from django.urls import path

from .views import LoginViews

app_name = 'gatewall'
urlpatterns = [
    path('kimlik/', LoginViews.Login.as_view(), name='login'),
]