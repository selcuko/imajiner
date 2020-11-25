from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

def handle404(request):
    return render(request, '404.html', {
        'doc': 
            {'title': _('You lost')}
    })