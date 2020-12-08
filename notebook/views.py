import json
import logging
import time
from uuid import UUID

from django.conf import settings
from django.conf.locale import LANG_INFO
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.shortcuts import Http404, HttpResponse, get_object_or_404
from django.shortcuts import redirect as dj_redirect
from django.shortcuts import render, reverse
from django.utils.translation import get_language_from_request
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from tagmanager.models import *

from .forms import NarrativeForm
from .models import Narrative, NarrativeTranslation

logger = logging.getLogger(__name__)


class Redirect(View):
    def get(self, request, uuid, *args, **kwargs):
        narrative = Narrative.objects.get(uuid=uuid)
        translation = narrative.translations.last()
        return dj_redirect(translation)


class Detail(DetailView):
    model = NarrativeTranslation
    context_object_name = 'narrative'
    template_name = 'notebook/narrative/detail.html'

    def get_object(self):
        self.slug = self.kwargs['slug']
        self.narrative = get_object_or_404(
            NarrativeTranslation, slug=self.slug)
        return self.narrative

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'doc': {
                'title': self.narrative.title,
                'author': self.narrative.master.author.username,
                'description': self.narrative.lead,
            },
            'LANG_INFO': LANG_INFO,
        })
        return ctx

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        try:
            if not request.user.is_authenticated:
                raise SuspiciousOperation('Unauthorized')

            narrative = request.POST['narrative']
            narrative = Narrative.objects.get(slug=narrative)

            if action == 'tag-create':
                abstract = request.POST['name']
                try:
                    abstract = AbstractTag.objects.get(name=abstract)
                except:
                    abstract = AbstractTag.objects.create(name=abstract)
                narrative.tags.add(abstract)
                request.user.tags.delta_for(
                    abstract=abstract, narrative=narrative, delta=1)
                return HttpResponse()

            elif action == 'tag-step':
                abstract = request.POST['name']
                request.user.tags.delta_for(
                    narrative=narrative, abstract=abstract, delta=1)
                return HttpResponse()

        except Exception as e:
            raise e


class List(ListView):
    model = NarrativeTranslation
    context_object_name = 'narratives'
    template_name = 'notebook/narrative/list.html'
    paginate_by = 20
    ordering = ('published_at',)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'doc': {
                'title': _('narratives').capitalize(),
                'author': self.request.user.username,
                'description': _('view the latest narratives published on Imajiner').capitalize()
            },
            'LANG_INFO': LANG_INFO,
        })
        return ctx

    def get_queryset(self):
        languages = [get_language_from_request(self.request, check_path=True)]
        if self.request.user.is_authenticated and self.request.user.profile.languages:
            languages += self.request.user.profile.languages
        base_qs = NarrativeTranslation.objects.filter(
            sketch=False,
            master__author__isnull=False,
        )
        qs = base_qs.filter(language__in=languages)
        if self.request.user.is_authenticated:
            qs = qs | base_qs.filter(
                master__author=self.request.user, sketch=False)
        return qs


class Folder(LoginRequiredMixin, View):
    template_name = 'notebook/narrative/folder.html'

    def get(self, request):
        NarrativeTranslation.objects.filter(
            sketch=True, master__author=request.user, title='', body__isnull=True).delete()
        sketches = NarrativeTranslation.objects.filter(
            sketch=True, master__author=request.user).order_by('-edited_at')
        return render(request, self.template_name, {
            'sketches': sketches,
            'no_sketch': not sketches.exists(),
        })


class FreshWrite(LoginRequiredMixin, View):
    template_name = 'notebook/narrative/write.html'

    def get(self, request):
        master = Narrative(sketch=True, author=request.user)
        master.save()
        sketch = NarrativeTranslation()
        sketch.reference(master)
        sketch.save()
        form = NarrativeForm(instance=sketch)

        return render(self.request, self.template_name, context={
            'form': form,
            'doc': {
                'title': _('refreshing the ink').capitalize()
            }
        })

    def post(self, request):
        try:
            uuid = request.POST['uuid']
            sketch = NarrativeTranslation.objects.get(
                uuid=uuid, master__author=request.user)
            form = NarrativeForm(request.POST, request.FILES, instance=sketch)

            action = request.POST.get('action', '').lower()

            if not form.is_valid():
                logger.warn('NarrativeForm is not valid.')
                return JsonResponse({}, status=400)

            if action == 'autosave':
                # Avoid creating new versions on every autosave.
                narrative = form.save(commit=False)
                narrative.save(new_version=False)
                return JsonResponse({'description': 'OK'})

            elif action == 'submit':
                narrative = form.save(commit=False)
                narrative.sketch = False
                narrative.save()
                response = {
                    'language': settings.LANGUAGES_DICT.get(narrative.language, narrative.language),
                    'publicUrl': narrative.get_absolute_url(),
                }
                return JsonResponse(response)

            else:  # action id not recognized or absent
                logger.warn('NarrativeForm submitted with no known action ID.')
                return JsonResponse({}, status=400)

        except KeyError as ke:
            logger.warn(f'NarrativeView encountered KeyError: {ke.__repr__()}')
            return JsonResponse({}, status=400)


class ContinueSketch(LoginRequiredMixin, View):
    template_name = 'notebook/narrative/write.html'

    def get(self, request, uuid):
        try:
            sketch = NarrativeTranslation.objects.get(
                uuid=uuid, master__author=request.user)
            form = NarrativeForm(instance=sketch)
        except NarrativeTranslation.DoesNotExist:
            return HttpResponse(status=404)
        return render(self.request, self.template_name, context={
            'form': form,
            'doc': {
                'title': _('refreshing the ink').capitalize()
            }
        })

    def post(self, request, uuid):
        try:
            uuid = request.POST['uuid']
            sketch = NarrativeTranslation.objects.get(
                uuid=uuid, master__author=request.user)
            form = NarrativeForm(request.POST, request.FILES, instance=sketch)

            action = request.POST.get('action', '').lower()

            if not form.is_valid():
                logger.warn('NarrativeForm is not valid.')
                return JsonResponse({}, status=400)

            if action == 'autosave':
                narrative = form.save(commit=False)
                narrative.save(new_version=False)
                return JsonResponse({'description': 'OK'})

            elif action == 'submit':
                narrative = form.save(commit=False)
                narrative.sketch = False
                narrative.save()
                response = {
                    'language': settings.LANGUAGES_DICT.get(narrative.language, narrative.language),
                    'publicUrl': narrative.get_absolute_url(),
                }
                return JsonResponse(response)

            else:  # action id not recognized or absent
                logger.warn('NarrativeForm submitted with no known action ID.')
                return JsonResponse({}, status=400)

        except KeyError as ke:
            logger.warn(f'NarrativeView encountered KeyError: {ke.__repr__()}')


class AddTranslation(LoginRequiredMixin, View):
    template_name = 'notebook/narrative/write.html'

    def get(self, request, uuid, redirect=False):
        if redirect:
            master = Narrative.objects.get(uuid=uuid, author=request.user)
            translation = NarrativeTranslation(master=master)
            translation.save()
            link = reverse('notebook:translate', kwargs={
                           'uuid': translation.uuid})
            return dj_redirect(to=link)

        translation = NarrativeTranslation.objects.get(uuid=uuid)
        form = NarrativeForm(instance=translation)
        return render(self.request, self.template_name, {
            'form': form,
            'doc': {
                'title': _('Translation')
            }
        })

    def post(self, request, uuid, redirect=None):

        translation = NarrativeTranslation.objects.get(uuid=uuid)
        form = NarrativeForm(request.POST, instance=translation)
        action = request.POST.get('action', '').lower()

        if not form.is_valid():
            logger.warn('NarrativeForm (Translation) not valid.')
            return JsonResponse({}, status=400)

        if action == 'submit':
            translation = form.save(commit=False)
            translation.sketch = False
            translation.save()
            response = {
                'language': settings.LANGUAGES_DICT.get(translation.language, translation.language),
                'publicUrl': translation.get_absolute_url(),
            }
            return JsonResponse(response)

        elif action == 'autosave':
            translation = form.save(commit=False)
            translation.sketch = True
            translation.save(new_version=False)
            return JsonResponse({})

        else:  # action id not recognized or absent
            logger.warn('NarrativeForm submitted with no known action ID.')
            return JsonResponse({}, status=400)
