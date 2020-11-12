from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static, serve
from explore.views import Home
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf.urls.i18n import i18n_patterns

LoginRequiredMixin.redirect_field_name = 'sonraki'

admin.site.site_header = 'Imajiner God View'
admin.site.site_title = 'Imajiner God View'
admin.site.index_title = 'Site Supervision'

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', Home.as_view(), name='landing'),
    path('', include('notebook.urls', namespace='narrative')),
    path('', include('gatewall.urls', namespace='gatewall')),
    path('', include('explore.urls', namespace='explore')),
    path('', include('identity.urls', namespace='identity')),
    path('', include('tagmanager.urls', namespace='tag')),
    path('', include('console.urls', namespace='console')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
