from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from .models import AbstractTag

class TagDetail(DetailView):
    model = AbstractTag
    lookup_field = 'slug'
    template_name = 'tag/detail.html'
    context_object_name = 'tag'


class TagList(ListView):
    model = AbstractTag
    template_name = 'tag/list.html'
    context_object_name = 'tags'