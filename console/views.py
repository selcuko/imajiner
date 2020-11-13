from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .context import *
from notebook.models import Narrative as NarrativeModel
from notebook.models import NarrativeVersion as NarrativeVersionModel
from identity.forms import ProfileForm
from notebook.forms import NarrativeForm
import logging

logger = logging.getLogger(__name__)

class Overview(LoginRequiredMixin, View):
    template = 'console/overview.html'

    def get(self, request):
        return render(request, self.template)


class Profile(LoginRequiredMixin, View):
    template = 'console/profile.html'

    def get(self, request):
        return render(request, self.template, {
            'form': ProfileForm(instance=request.user.profile)
        })
    
    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            
        return render(request, self.template, {
                'form': form
            })

class Access(View):
    template = 'console/access.html'
    def get(self, request):
        return render(request, self.template)
    
    def post(self, request):
        print(request.POST)
        if 'basics' in request.POST:
            print('access:basics')
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            if username:
                request.user.username = username
                request.user.save()
            if password:
                request.user.set_password(password)
        return render(request, self.template)

class Narratives(View):
    template = 'console/narratives.html'
    def get(self, request):
        return render(request, self.template)
class Narrative(View):
    template = 'console/narrative.html'
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

class NarrativeVersions(View):
    template = 'console/narrative/versions.html'
    def get(self, request, narrative):
        narrative = NarrativeModel.objects.get(uuid=narrative)
        return render(request, self.template, {'narrative': narrative})

class NarrativeVersion(View):
    template = 'console/narrative/readonly.html'
    def get(self, request, narrative, version):
        version = NarrativeVersionModel.objects.get(uuid=version)
        return render(request, self.template, {'version': version})

class Sketches(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)
class Sketch(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)

class Medium(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)
class Media(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)

class Series(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)
class Serie(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)


class Subscriptions(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)

class Preferences(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)

class Studio(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)

class Refereeship(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)

