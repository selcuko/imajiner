from django.urls import path
from .views import TagDetail, TagList

app_name = 'tag'
urlpatterns = [
    path('leybıl/<slug:slug>/', TagDetail.as_view(), name='detail'),
    path('leybıl/', TagList.as_view(), name='list'),
]