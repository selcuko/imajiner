from django.shortcuts import render, HttpResponse
from django.views import View


class Home(View):
    template_name = 'explore/home.html'
    def get(self, request, **kwargs):
        return render(request, self.template_name, {})
    
    def post(self, request):
        return HttpResponse(status_code=403)
