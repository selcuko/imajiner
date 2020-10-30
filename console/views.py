from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class Console(LoginRequiredMixin, View):
    template = 'console/overview.html'

    def get(self, request):
        user = request.user
        highlights = user.narratives.all()[:5]
        return render(request, self.template, {
            'highlights': highlights
        })
