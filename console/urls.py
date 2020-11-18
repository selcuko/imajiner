from django.urls import path
from .views import *
from django.utils.translation import gettext_lazy as _

app_name = 'console'

urlpatterns = [
    path('', Overview.as_view(), name='overview'),
    path(_('iam/'), Profile.as_view(), name='profile'),
    path(_('access/'), AccessSecurity.as_view(), name='access'),
    path(_('narratives/'), Narratives.as_view(), name='narratives'),
    path(_('narratives/<uuid:narrative>/'), Narrative.as_view(), name='narrative'),
    path(_('narratives/<uuid:narrative>/versions/'), NarrativeVersions.as_view(), name='versions'),
    path(_('narratives/<uuid:narrative>/versions/<uuid:version>/'), NarrativeVersion.as_view(), name='version'),
    path(_('refereeship/'), Refereeship.as_view(), name='refereeship'),
    path(_('studio/'), Studio.as_view(), name='studio'),
    path(_('subscriptions/'), Subscriptions.as_view(), name='subscriptions'),
    path(_('preferences/'), Preferences.as_view(), name='preferences'),
]