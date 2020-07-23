from django.shortcuts import render
from django.views.generic import DetailView
from .models import Narrative


class NarrativeViews:
    class Detail(DetailView):
        models = Narrative
        context_object_name = 'narrative'
        template_name = 'notebook/narrative/detail.html'

        def get_queryset(self):
            slug = self.kwargs['slug']
            return Narrative.objects.get(slug=slug)