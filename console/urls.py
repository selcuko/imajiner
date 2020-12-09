from django.urls import path
from .views import *
from django.utils.translation import gettext_lazy as _

app_name = 'console'

urlpatterns = [
    path('', Overview.as_view(), name='overview'),
    path(_('iam/'), Profile.as_view(), name='profile'),
    path(_('access/'), AccessSecurity.as_view(), name='access'),

    path(_('narratives/'),                       Narratives.as_view(), name='narratives'),
    path(_('n/<uuid:n_uuid>/'),                  NarrativeDetail.as_view(), name='narrative-latest'),
    path(_('n/<uuid:n_uuid>/languages/'),        NarrativeTranslations.as_view(), name='narrative-translations'),
    path(_('n/<uuid:n_uuid>/versions/'),         NarrativeTimeline.as_view(), name='narrative-timeline'),
    path(_('n/<uuid:n_uuid>/v/<uuid:v_uuid>/'),  NarrativeVersionDetail.as_view(), name='narrative-version'),
    
    path(_('preferences/'), Preferences.as_view(), name='preferences'),
]