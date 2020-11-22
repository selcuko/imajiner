from django.contrib.sitemaps import Sitemap
from .models import *

class NarrativeSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return NarrativeTranslation.objects.filter(sketch=False)

    def lastmod(self, obj):
        return obj.published_at