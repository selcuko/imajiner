from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.models import User
from notebook.models import *
from .models import *

class AuthorView(DetailView):
    model = User
    context_object_name = 'author'
    template_name = 'identity/author.html'

    def get_object(self, *args, **kwargs):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['narratives'] = NarrativeTranslation.objects.of(author=self.object)
        return context
