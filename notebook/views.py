from django.shortcuts import render, HttpResponse, redirect, reverse, Http404
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Narrative, NarrativeTranslation, SoundRecord
from .forms import NarrativeForm, SoundUploadForm
from tagmanager.models import *
import json
from uuid import UUID
from django.core.exceptions import SuspiciousOperation
from django.utils.translation import gettext as _, get_language_from_request



class NarrativeRedirect(View):
    def get(self, request, uuid, *args, **kwargs):
        narrative = Narrative.objects.get(uuid=uuid)
        translation = narrative.translations.last()
        return redirect(translation)



class NarrativeDetail(DetailView):
    model = NarrativeTranslation
    context_object_name = 'narrative'
    template_name = 'notebook/narrative/detail.html'

    def get_object(self):
        self.slug = self.kwargs['slug']
        self.narrative = NarrativeTranslation.objects.get(slug=self.slug)
        return self.narrative
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'doc': {
                'title': self.narrative.title,
                'author': self.narrative.master.author.username,
            }
        })
        return ctx
    
    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        try:
            if not request.user.is_authenticated: raise SuspiciousOperation('Unauthorized')

            narrative = request.POST['narrative']
            narrative = Narrative.objects.get(slug=narrative)

            if action == 'tag-create':
                abstract = request.POST['name']
                try:
                    abstract = AbstractTag.objects.get(name=abstract)
                except:
                    abstract = AbstractTag.objects.create(name=abstract)
                narrative.tags.add(abstract)
                request.user.tags.delta_for(abstract=abstract, narrative=narrative, delta=1)
                return HttpResponse()
            
            elif action == 'tag-step':
                abstract = request.POST['name']
                request.user.tags.delta_for(narrative=narrative, abstract=abstract, delta=1)
                return HttpResponse()

        except Exception as e:
            raise e
    


class NarrativeList(ListView):
    model = NarrativeTranslation
    context_object_name = 'narratives'
    template_name = 'notebook/narrative/list.html'
    paginate_by = 12
    ordering = ('published_at',)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'doc': {
                'title': _('narratives').capitalize(),
                'author': ''
            }
        })
        return ctx

    def get_queryset(self):
        languages = [get_language_from_request(self.request, check_path=True)]
        if self.request.user.is_authenticated and self.request.user.profile.languages:
            languages += self.request.user.profile.languages.split(':')
        qs = NarrativeTranslation.objects.filter(
                sketch=False, 
                master__author__isnull=False,
                language__in=languages)
        if self.request.user.is_authenticated:
            qs = qs | NarrativeTranslation.objects.filter(master__author=self.request.user)
        return qs



class NarrativeWrite(LoginRequiredMixin, View):
    template_name = 'notebook/narrative/write.html'

    def get(self, request, uuid=None):
        new = not bool(uuid)
        if new:
            sketch = Narrative(sketch=True, author=request.user)
            sketch.save()
            print('Created with UUID', sketch.uuid)
            form = NarrativeForm(instance=sketch)
        else:
            try:
                sketch = Narrative.objects.get(uuid=uuid, author=request.user)
                form = NarrativeForm(instance=sketch)
            except Narrative.DoesNotExist:
                return HttpResponse(status=404)
                
        return render(self.request, self.template_name, context={
            'form': form,
            'doc': {
                'title': _('refreshing the ink').capitalize()
            }
            })

    def post(self, request, uuid=None):
        new = not bool(uuid)

        if new:
            uuid = request.POST['uuid']
            print('UUID', uuid)
            sketch = Narrative.objects.get(uuid=uuid, sketch=True, author=request.user)
            form = NarrativeForm(request.POST, request.FILES, instance=sketch)
        else:
            try:
                sketch = Narrative.objects.get(uuid=uuid, sketch=True, author=request.user)
                form = NarrativeForm(request.POST, request.FILES, instance=sketch)
                print('Returning sketch:', sketch.title)
            except:
                return HttpResponse(status=404)
        
        action = request.POST.get('action', 'submit').lower()
        
        if not form.is_valid():
            return render(self.request, self.template_name, context={'form':form})
        
        if action == 'submit':
            narrative = form.save(commit=False)
            narrative.sketch = False
            narrative.save()
            return redirect(narrative.translations.last())
        
        elif action == 'autosave':
            form.save()
            return HttpResponse()
        
        else:
            raise Exception('Action ID unknown')
        
        

class NarrativeFolder(LoginRequiredMixin, View):
    template_name = 'notebook/narrative/folder.html'
    def get(self, request):
    
        sketches = Narrative.objects.filter(sketch=True, author=request.user)
        return render(request, self.template_name, {
            'sketches': sketches,
            'no_sketch': not sketches.exists(),
        })


    
