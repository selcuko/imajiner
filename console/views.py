from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .context import *

class Overview(LoginRequiredMixin, View):
    template = 'console/overview.html'

    def get(self, request):
        return render(request, self.template)


class Profile(LoginRequiredMixin, View):
    template = 'console/profile.html'

    def get(self, request):
        return render(request, self.template)


class Narratives(View):
    template = 'console/narratives.html'

    def get(self, request):
        ctx = user_content(user)
        return render(request, self.template)


class Series(View):
    template = 'console/series.html'

    def get(self, request):
        return render(request, self.template)
