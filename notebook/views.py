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
from django.shortcuts import redirect
from django.shortcuts import render, reverse
from django.utils.translation import get_language_from_request
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from tagmanager.models import *

from .forms import NarrativeForm
from .models import Narrative, NarrativeTranslation

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Redirect(View):
    def get(self, request, uuid, *args, **kwargs):
        narrative = Narrative.objects.get(uuid=uuid)
        translation = narrative.translations.last()
        return redirect(translation)



class Detail(DetailView):
    model = NarrativeTranslation
    context_object_name = 'narrative'
    template_name = 'notebook/narrative/detail.html'
    lookup_field = 'slug'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'doc': {
                'title': self.object.title,
                'author': self.object.master.author.username,
                'description': self.object.lead,
            },
            'LANG_INFO': LANG_INFO,
        })
        return ctx



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
        return NarrativeTranslation.objects.public()


class Folder(LoginRequiredMixin, ListView):
    template_name = 'notebook/narrative/folder.html'
    model = NarrativeTranslation
    context_object_name = 'sketches'
    ordering = ('-edited_at',)

    def get_queryset(self, *args, **kwargs):
        return NarrativeTranslation.objects.sketches(author=self.request.user)


class FreshWrite(LoginRequiredMixin, View):
    template_name = 'notebook/narrative/write.html'

    def get(self, request, uuid=None):
        if uuid:
            try:
                narrative = NarrativeTranslation.objects.sketch(uuid=uuid, author=request.user)
            except NarrativeTranslation.DoesNotExist:
                return JsonResponse({}, status=404)
        else:
            narrative = NarrativeTranslation()
            narrative.save(author=request.user)
        form = NarrativeForm(instance=narrative)

        return render(self.request, self.template_name, context={
            'form': form,
            'doc': {
                'title': _('refreshing the ink').capitalize()
            }})

    def post(self, request, uuid=None):
        try:
            if not uuid:
                uuid = request.POST['uuid']
            try:
                narrative = NarrativeTranslation.objects.sketch(uuid=uuid, author=request.user)
            except NarrativeTranslation.DoesNotExist:
                return JsonResponse({}, status=404)
            action = request.POST['action'].lower()
            
            form = NarrativeForm(request.POST, instance=narrative)

            if not form.is_valid():
                logger.warning(f'NarrativeForm is not valid: {form.errors}')
                return JsonResponse(dict(form.errors), status=400)

            if action == 'autosave':
                narrative = form.save(commit=False)
                narrative.autosave()
                return JsonResponse({})

            elif action == 'submit':
                narrative = form.save(commit=False)
                narrative.publish()
                response = {
                    'language': settings.LANGUAGES_DICT.get(narrative.language, narrative.language),
                    'publicUrl': narrative.get_absolute_url(),
                }
                return JsonResponse(response)

            else:  # action id not recognized or absent
                logger.warning(f'NarrativeForm submitted with no known action ID: {action}')
                return JsonResponse({}, status=400)

        except KeyError as exc:
            logger.warning(f'NarrativeView encountered KeyError: {exc!r}')
            return JsonResponse({}, status=400)


class AddTranslation(LoginRequiredMixin, View):

    def get(self, request, uuid):
        referrer = NarrativeTranslation.objects.get(uuid=uuid)
        translation = NarrativeTranslation(master=referrer.master)
        translation.save()
        return redirect(to=reverse('narrative:sketch', kwargs={'uuid': translation.uuid}))

