from django.conf import settings
from django import template

GA_ID = settings.GOOGLE_ANALYTICS_ID

register = template.Library()

@register.simple_tag
def google_analytics():
    return f"""<script async src="https://www.googletagmanager.com/gtag/js?id=UA-174465907-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());gtag('config', 'UA-174465907-1');</script>"""