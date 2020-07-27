from django.shortcuts import render, HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login

class LoginViews:

    class Login(View):

        def get(self, request):
            return render(request, 'gatewall/login.html')
        
        def post(self, request):
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(request, username=username, password=password)
            if user is None:
                return HttpResponse('Siktir git yalancı')
            login(request, user)
            return HttpResponse('Giriş yaptın yavru')


