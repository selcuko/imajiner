from django.shortcuts import render
from .models import *

def author_view(request, username):
    user = User.objects.get(username=username)
    return render(request, 'identity/author.html', {'user': user})

