from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static, serve
from explore.views import Home
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.contrib.sitemaps.views import sitemap
from notebook.sitemap import NarrativeSitemap
from django.views.i18n import JavaScriptCatalog
from explore.views import Feedback

admin.site.site_header = _('Imajiner God View')
admin.site.site_title = _('Imajiner God View')
admin.site.index_title = _('Site Supervision')

admin.site.empty_value_display = 'NULL'

LoginRequiredMixin.redirect_field_name = 'n'

handle404 = 'imajiner.views.handle404'

urlpatterns = [
    path('@/', admin.site.urls),
    path('feedback/', Feedback.as_view(), name='feedback'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('sitemap.xml', sitemap, {'sitemaps': {'notebook': NarrativeSitemap }},
     name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += i18n_patterns(
    path('', Home.as_view(), name='landing'),
    path(_('narratives/'), include('notebook.urls', namespace='narrative')),
    path('', include('gatewall.urls', namespace='gatewall')),
    path('', include('explore.urls', namespace='explore')),
    path('', include('identity.urls', namespace='identity')),
    path('', include('tagmanager.urls', namespace='tag')),
    path(_('console/'), include('console.urls', namespace='console')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
