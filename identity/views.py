from django.shortcuts import render
from .models import *

def author_view(request, username):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        u = None
    return render(request, 'identity/author.html', {'author': u})
