from django.shortcuts import render
from notebook.models import Narrative
from .models import *

def author_view(request, username):
    user = User.objects.get(username=username)
    return render(request, 'identity/author.html', {
        'user': user,
        'narratives': NarrativeTranslation.objects.filter(master__author=user, sketch=False),
        })


def self_view(request):
    return render(request, 'identity/self.html')

