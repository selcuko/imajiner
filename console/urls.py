from django.urls import path
from .views import *
from django.utils.translation import gettext_lazy as _

app_name = 'console'

urlpatterns = [
    path('', Overview.as_view(), name='overview'),
    path(_('iam/'), Profile.as_view(), name='profile'),
    path(_('access/'), AccessSecurity.as_view(), name='access'),

    # all narratives
    path(_('narratives/'),                       Narratives.as_view(), name='narratives'),
    # translations of a particular narrative
    path(_('n/<uuid:n_uuid>/'),                  NarrativeTranslations.as_view(), name='narrative-translations'),
    # detail of a narrative-translation
    path(_('n/<uuid:n_uuid>/l/<uuid:t_uuid>/'),  NarrativeDetail.as_view(), name='narrative-detail'),
    # timeline of a narrative-translation
    path(_('n/<uuid:n_uuid>/l/<uuid:t_uuid>/timeline/'), NarrativeTimeline.as_view(), name='narrative-timeline'),
    # detail of a narrative-version
    path(_('n/<uuid:n_uuid>/v/<uuid:v_uuid>/'),  NarrativeVersionDetail.as_view(), name='narrative-version'),
    
    path(_('preferences/'), Preferences.as_view(), name='preferences'),
]