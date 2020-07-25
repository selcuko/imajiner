from django.shortcuts import render, HttpResponse
from django.views.generic import DetailView
from .models import Narrative
import json


class NarrativeViews:
    class Detail(DetailView):
        model = Narrative
        context_object_name = 'narrative'
        template_name = 'notebook/narrative/detail.html'

        def get_object(self):
            slug = self.kwargs['slug']
            self.narrative = Narrative.objects.get(slug=slug)
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
            print(f'Clicked on {slug} by {user} for {amount} times')