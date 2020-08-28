from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static, serve
from explore.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', Home.as_view(), name='landing'),
    path('', include('notebook.urls', namespace='narrative')),
    path('', include('gatewall.urls', namespace='gatewall')),
    path('', include('explore.urls', namespace='explore')),
    path('', include('identity.urls', namespace='identity')),
    path('', include('evangelism.urls', namespace='evangelism')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
