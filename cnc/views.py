from django.shortcuts import render
from django.views import View

class CommandAndControl(View):
    template = 'cnc/cncpanel.html'
    ctx = {
        'doc': {'title': 'Komuta'}
    }

    def get(self, request):
        return render(request, self.template, self.ctx)

