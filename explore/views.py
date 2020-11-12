from django.shortcuts import render, HttpResponse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from notebook.models import Narrative
from django.conf import settings
from django.http import HttpResponsePermanentRedirect



def red(request):
    return HttpResponsePermanentRedirect(f'https://{settings.PRIMARY_HOST}')

class Home(View):
    template_name = 'landing.html'
    def get(self, request, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request):
        return HttpResponse(status_code=403)


class Infinite(View):
    template_name = 'explore/inf.html'
    numbers_all = Narrative.objects.all()
    paginator = Paginator(numbers_all, 2)

    def get(self, request):
        page = request.GET.get('page', 1)
        try:
            numbers = self.paginator.page(page)
        except PageNotAnInteger:
            numbers = self.paginator.page(1)
        except EmptyPage:
            numbers = self.paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'numbers': numbers})
