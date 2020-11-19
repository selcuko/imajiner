from django.shortcuts import render
from django.views import View
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .context import *
from notebook.models import Narrative as NarrativeModel
from notebook.models import NarrativeVersion as NarrativeVersionModel
from identity.forms import ProfileForm
from notebook.forms import NarrativeForm
import logging
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)

class Overview(LoginRequiredMixin, View):
    template = 'console/overview.html'
    document = {
        'title': _('console overview').title(),
    }

    def get(self, request):
        return render(request, self.template, {'doc': self.document})


class Profile(LoginRequiredMixin, View):
    template = 'console/profile.html'
    document = {
        'title': _('profile').title(),
    }

    def get(self, request):
        return render(request, self.template, {
            'form': ProfileForm(instance=request.user.profile),
            'doc': self.document,
        })
    
    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            
        return render(request, self.template, {
                'form': form,
                'doc': self.document,
            })

class AccessSecurity(LoginRequiredMixin, View):
    template = 'console/access.html'
    document = {
        'title': _('access & security').title(),
    }
    def get(self, request):
        return render(request, self.template, {'doc': self.document})
    
    def post(self, request):
        print(request.POST)
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
        return render(request, self.template, {'doc': self.document})

class Narratives(LoginRequiredMixin, View):
    document = {
        'title': _('my narratives').capitalize(),
    }
    template = 'console/narratives.html'
    def get(self, request):
        return render(request, self.template, {'doc': self.document})
class Narrative(LoginRequiredMixin, View):
    template = 'console/narrative.html'
    document = {
        'title': _('edit narrative').capitalize(),
    }
    def get(self, request, narrative):
        narrative = NarrativeModel.objects.get(author=request.user, uuid=narrative)
        form = NarrativeForm(instance=narrative)
        return render(request, self.template, {'form': form,'narrative': narrative})
    
    def post(self, request, narrative):
        narrative = NarrativeModel.objects.get(author=request.user, uuid=narrative)
        form = NarrativeForm(request.POST, instance=narrative)
        if form.is_valid(): 
            narrative = form.save(commit=False)
            narrative.save(new_version=True)
        else:
            print('FORM INVALID')
            print(form.errors)
        return render(request, self.template, {'form': form,'narrative': narrative})

class NarrativeVersions(LoginRequiredMixin, View):
    template = 'console/narrative/versions.html'
    document = {
        'title': _('narrative version timeline').capitalize(),
    }
    def get(self, request, narrative):
        narrative = NarrativeModel.objects.get(uuid=narrative)
        return render(request, self.template, {'narrative': narrative})

class NarrativeVersion(LoginRequiredMixin, View):
    template = 'console/narrative/readonly.html'
    document = {
        'title': _('narrative version history').capitalize(),
    }
    def get(self, request, narrative, version):
        version = NarrativeVersionModel.objects.get(uuid=version)
        return render(request, self.template, {'version': version})

class Sketches(LoginRequiredMixin, View):
    template = 'console/blank.html'
    document = {
        'title': _('console').capitalize(),
    }
    def get(self, request):
        return render(request, self.template, {'doc': self.document})
class Sketch(LoginRequiredMixin, View):
    template = 'console/blank.html'
    document = {
        'title': _('console').capitalize(),
    }
    def get(self, request):
        return render(request, self.template, {'doc': self.document})

class Medium(LoginRequiredMixin, View):
    template = 'console/blank.html'
    document = {
        'title': _('console').capitalize(),
    }
    def get(self, request):
        return render(request, self.template, {'doc': self.document})
class Media(LoginRequiredMixin, View):
    template = 'console/blank.html'
    document = {
        'title': _('console').capitalize(),
    }
    def get(self, request):
        return render(request, self.template, {'doc': self.document})

class Series(LoginRequiredMixin, View):
    template = 'console/blank.html'
    document = {
        'title': _('console').capitalize(),
    }
    def get(self, request):
        return render(request, self.template, {'doc': self.document})
class Serie(LoginRequiredMixin, View):
    template = 'console/blank.html'
    document = {
        'title': _('console').capitalize(),
    }
    def get(self, request):
        return render(request, self.template, {'doc': self.document})


class Subscriptions(LoginRequiredMixin, View):
    template = 'console/blank.html'
    document = {
        'title': _('console').capitalize(),
    }
    def get(self, request):
        return render(request, self.template, {'doc': self.document})

class Preferences(LoginRequiredMixin, View):
    template = 'console/preferences.html'
    lang_codes = [l[0] for l in settings.LANGUAGES]
    document = {
        'title': _('console').capitalize(),
    }

    def get(self, request):
        return render(request, self.template, {'settins': settings})
    
    def post(self, request):
        action = request.POST.get('action', None)
        if not action: raise SuspiciousOperation

        try:
            if action == 'set-primary-language':
                language = request.POST.get('language-code')
                if not language in self.lang_codes: raise SuspiciousOperation
                request.user.profile.language = language
                request.user.save()
        except: raise SuspiciousOperation

        return HttpResponse()

class Studio(LoginRequiredMixin, View):
    template = 'console/blank.html'
    document = {
        'title': _('console').capitalize(),
    }
    def get(self, request):
        return render(request, self.template, {'doc': self.document})

class Refereeship(LoginRequiredMixin, View):
    template = 'console/blank.html'
    document = {
        'title': _('console').capitalize(),
    }
    def get(self, request):
        return render(request, self.template, {'doc': self.document})

