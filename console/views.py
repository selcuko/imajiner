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

class Access(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)

class Narratives(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)
class Narrative(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)

class Sketches(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)
class Sketch(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)

class Medium(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)
class Media(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)

class Series(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)
class Serie(View):
    template = 'console/blank.html'
    def get(self, request):
        return render(request, self.template)
