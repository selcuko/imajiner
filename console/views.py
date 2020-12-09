from django.shortcuts import render
from django.views import View
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .context import *
from notebook.models import Narrative as NarrativeModel
from notebook.models import NarrativeVersion as NarrativeVersionModel
from notebook.models import NarrativeTranslation as NarrativeTranslationModel
from identity.forms import ProfileForm
from notebook.forms import NarrativeForm
import logging
import time
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


class Overview(LoginRequiredMixin, View):
    template = 'console/overview.html'

    def get(self, request):
        return render(request, self.template, {
            'doc': {
                'title': _('console overview').title(),
            }
        })


class Profile(LoginRequiredMixin, View):
    template = 'console/profile.html'

    def get(self, request):
        return render(request, self.template, {
            'form': ProfileForm(instance=request.user.profile),
            'doc':{
                'title': _('profile').title(),
            }
        })
    
    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
        else:
            logger.warn('ProfileForm not valid.')
            
        return render(request, self.template, {
            'form': form,
            'doc': {
                'title': _('profile').title(),
            }
        })


class AccessSecurity(LoginRequiredMixin, View):
    template = 'console/access.html'

    def get(self, request):
        return render(request, self.template, {
            'doc': {
                'title': _('access & security').title(),
            }
        })
    
    def post(self, request):
        time.sleep(2)
        
        if 'basics' in request.POST:
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            if username:
                request.user.username = username
                request.user.save()
            if password:
                request.user.set_password(password)

        elif 'session_key' in request.POST:
            try: Session.objects.get(session_key=request.POST['session_key']).delete()
            except Session.DoesNotExist: pass

        return render(request, self.template, {
            'doc': {
                'title': _('access & security').title(),
            }
        })


class Narratives(LoginRequiredMixin, View):
    template = 'console/narratives.html'

    def get(self, request):
        return render(request, self.template, {
            'doc': {
                'title': _('my narratives').capitalize(),
            }
        })


class Narrative(LoginRequiredMixin, View):
    template = 'console/narrative.html'

    def get(self, request, n_uuid):
        narrative = NarrativeModel.objects.get(author=request.user, uuid=n_uuid)
        form = NarrativeForm(instance=narrative)
        return render(request, self.template, {
            'form': form,
            'narrative': narrative,
            'doc':{
                'title': _('edit narrative').capitalize(),
            }
        })
    
    def post(self, request, n_uuid):
        narrative = NarrativeModel.objects.get(author=request.user, uuid=n_uuid)
        form = NarrativeForm(request.POST, instance=narrative)
        if form.is_valid(): 
            narrative = form.save(commit=False)
            narrative.save(new_version=True)
        return render(request, self.template, {
            'form': form,'narrative': narrative,
            'doc': {
                'title': _('edit narrative').capitalize(),
            }
        })


class NarrativeVersions(LoginRequiredMixin, View):
    template = 'console/narrative/versions.html'

    def get(self, request, n_uuid):
        narrative = NarrativeModel.objects.get(uuid=n_uuid)
        return render(request, self.template, {
            'narrative': narrative,
            'doc':{
                'title': _('narrative version timeline').capitalize(),
            }
        })

class NarrativeVersion(LoginRequiredMixin, View):
    template = 'console/narrative/readonly.html'

    def get(self, request, n_uuid, v_uuid):
        version = NarrativeVersionModel.objects.get(uuid=v_uuid)
        return render(request, self.template, {
            'version': version,
            'doc': {
                'title': _('narrative version history').capitalize(),
            }
        })



class Preferences(LoginRequiredMixin, View):
    template = 'console/preferences.html'
    lang_codes = set(settings.LANGUAGES_DICT.keys())

    def get(self, request):
        return render(request, self.template, {
            'settins': settings,
            'doc': {
                'title': _('preferences').capitalize(),
            }
        })
    
    def post(self, request):
        action = request.POST.get('action', None)
        time.sleep(2)

        if action == 'set-languages':
            languages = set(request.POST.get('language-codes').split(','))
            
            if not languages.issubset(self.lang_codes): 
                #SUS language options are predefined in settings.py
                raise SuspiciousOperation

            request.user.profile.languages = list(languages)
            request.user.profile.save()
        
        else:
            raise SuspiciousOperation('Action is not supplied in POST or recognized.')

        return HttpResponse()

