from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static, serve

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('notebook.urls', namespace='narrative')),
    path('', include('gatewall.urls', namespace='gatewall')),
]

if settings.DEBUG:
    #urlpatterns += [re_path(r'^static/(?P<path>.*)$', serve, {'show_indexes':True, 'document_root':settings.STATIC_ROOT})]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
