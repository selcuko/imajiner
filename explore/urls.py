from django.urls import path
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from .views import *

app_name = 'explore'
urlpatterns = [
    path('', Home.as_view(), name='home'),
    path(_('about/'), TemplateView.as_view(
        template_name='static/about.html',
        extra_context={'doc': {'title': _('About')}}), name='about'),
]