from django.urls import path

from .views import LoginViews, Auth

app_name = 'gatewall'
urlpatterns = [
    path('ben-kimim/', LoginViews.Login.as_view(), name='login'),
    path('seremoni/', LoginViews.Register.as_view(), name='register'),
    path('tc/', Auth.as_view(), name='tc')
]