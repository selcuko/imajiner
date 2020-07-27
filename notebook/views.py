from django.shortcuts import render, HttpResponse
from django.views.generic import DetailView, ListView
from .models import Narrative
import json


class NarrativeViews:
    class Detail(DetailView):
        model = Narrative
        context_object_name = 'narrative'
        template_name = 'notebook/narrative/detail.html'

        def get_object(self):
            self.slug = self.kwargs['slug']
            self.narrative = Narrative.objects.get(slug=self.slug)
            return self.narrative
        
        def post(self, request, *args, **kwargs):
            action = request.POST['action']
            payload = json.loads(request.POST['payload'])
            if action == 'TAGDELTA':
                for slug, delta in payload.items():
                    self.tag_delta(slug, delta)
            return HttpResponse()
        

        def tag_delta(self, slug, amount=1):
            user = self.request.user
            if not user.is_authenticated:
                return False
            user.tags.delta(
                slug=slug,
                diff=amount,
                narrative=self.kwargs['slug']
            )

    class List(ListView):
        model = Narrative
        context_object_name = 'narratives'
        template_name = 'notebook/narrative/list.html'

        def get_queryset(self):
            return Narrative.objects.all()