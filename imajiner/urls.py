from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from notebook.views import NarrativeViews

urlpatterns = [
    path('admin/', admin.site.urls),

    path('hikaye/<slug:slug>/', NarrativeViews.Detail.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
