from django.shortcuts import render, HttpResponse, redirect, reverse, Http404
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Narrative, SoundRecord
from .forms import NarrativeForm, SoundUploadForm
from tagmanager.models import *
import json
from uuid import UUID
from django.core.exceptions import SuspiciousOperation


class NarrativeDetail(DetailView):
    model = Narrative
    context_object_name = 'narrative'
    template_name = 'notebook/narrative/detail.html'

    def get_object(self):
        self.slug = self.kwargs['slug']
        self.narrative = Narrative.objects.get(slug=self.slug)
        return self.narrative
    
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'doc': {
                'title': self.narrative.title,
                'author': self.narrative.author.username,
            }
        })
        return ctx
    
    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        try:
            if not request.user.is_authenticated: raise SuspiciousOperation('Giriş yapılmamış')

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
    

    def tag_delta(self, slug, amount=1):
        user = self.request.user
        if not user.is_authenticated:
            return False
        user.tags.delta(
            slug=slug,
            diff=amount,
            narrative=self.kwargs['slug']
        )

class NarrativeList(ListView):
    model = Narrative
    context_object_name = 'narratives'
    template_name = 'notebook/narrative/list.html'
    paginate_by = 12
    ordering = ('created_at',)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'doc': {
                'title': 'Hikayeler',
                'author': 'Imajiner Müşterileri'
            }
        })
        return ctx

    def get_queryset(self):
        return Narrative.objects.filter(sketch=False, author__isnull=False).order_by('-created_at')



class NarrativeWrite(LoginRequiredMixin, View):
    template_name = 'notebook/narrative/write.html'

    def get(self, request, uuid=None):
        new = not bool(uuid)
        if new:
            sketch = Narrative(sketch=True, author=request.user)
            sketch.save()
            form = NarrativeForm(instance=sketch)
        else:
            try:
                sketch = Narrative.objects.get(uuid=uuid, sketch=True, author=request.user)
                form = NarrativeForm(instance=sketch)
            except Narrative.DoesNotExist:
                return HttpResponse(status=404)
                
        sounds = SoundRecord.objects.filter(uploader=request.user)
        return render(self.request, self.template_name, context={
            'form': form,
            'sounds': sounds,
            })

    def post(self, request, uuid=None):
        new = not bool(uuid)

        if new:
            uuid = request.POST['uuid']
            sketch = Narrative.objects.get(uuid=uuid, sketch=True, author=request.user)
            form = NarrativeForm(request.POST, request.FILES, instance=sketch)
        else:
            try:
                sketch = Narrative.objects.get(uuid=uuid, sketch=True, author=request.user)
                form = NarrativeForm(request.POST, request.FILES, instance=sketch)
            except:
                return HttpResponse(status=404)
        
        action = request.POST.get('action', 'submit').lower()
        
        if not form.is_valid():
            return render(self.request, self.template_name, context={'form':form})
        
        if action == 'submit':
            narrative = form.save(commit=False)
            narrative.sketch = False
            narrative.save()
            return redirect(narrative)
        
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


class SoundUpload(CreateView):
    template_name = 'notebook/upload.html'
    model = SoundRecord
    fields = [
        'name',
        'file',
    ]
    def get_success_url(self, *args, **kwargs):
        return ''

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)
    
