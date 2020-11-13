from django.urls import path
from .views import *
from django.utils.translation import gettext_lazy as _

app_name = 'console'

urlpatterns = [
    path('', Overview.as_view(), name='overview'),
    path(_('iam'), Profile.as_view(), name='profile'),
    path(_('access'), Access.as_view(), name='access'),
    path(f'{_("narratives")}', Narratives.as_view(), name='narratives'),
    path(f'{_("narratives")}/<uuid:uuid>/', Narrative.as_view(), name='narrative'),
    path(f'{_("narratives")}/<uuid:uuid>/{_("versions")}/', NarrativeVersions.as_view(), name='versions'),
    path(f'{_("narratives")}/<uuid:narrative>/{_("versions")}/<uuid:version>/', NarrativeVersion.as_view(), name='version'),
    path(_('sketches/'), Sketches.as_view(), name='sketches'),
    path(_('sketches/<uuid:uuid>/'), Sketch.as_view(), name='sketch'),
    path(_('series'), Series.as_view(), name='series'),
    path(_('series/<uuid:uuid>/'), Serie.as_view(), name='serie'),
    path(_('media/'), Medium.as_view(), name='medium'),
    path(_('media/<uuid:uuid>/'), Media.as_view(), name='media'),
    path(_('refereeship/'), Refereeship.as_view(), name='refereeship'),
    path(_('studio/'), Studio.as_view(), name='studio'),
    path(_('subscriptions/'), Subscriptions.as_view(), name='subscriptions'),
    path(_('preferences/'), Preferences.as_view(), name='preferences'),
]