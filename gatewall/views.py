from django.shortcuts import render, HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from uuid import uuid4 as uuid
from django.contrib.auth.models import User
from identity.models import Shadow

class LoginViews:

    class Login(View):

        def get(self, request):
            return render(request, 'gatewall/login.html')
        
        def post(self, request):
            action = request.POST['action']
            if action == 'LOGIN':
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                user = authenticate(request, username=username, password=password)
                if user is None:
                    return HttpResponse('Siktir git yalancı')
                login(request, user)
                return HttpResponse('Giriş yaptın yavru')
            
            elif action == 'SHADOW':
                shadow = Shadow.authenticate(request)
                if shadow is not None:
                    login(request, shadow.user)
                    return HttpResponse('Kayıt zaten vardı, nası oluyosa')
                shadow = Shadow.create_shadow(request)
                login(request, shadow.user)
                return HttpResponse('Oki shadow kayıt tamam')


    class Register(View):
        template_name = 'gatewall/register.html'
        def get(self, request):
            return render(request, self.template_name, {})
        

        def post(self, request):
            action = request.POST.get('action', '')
            username = request.POST.get('username', '')
            
            if action == 'REGULAR':
                password = request.POST.get('password', '')
                email = request.POST.get('email', None)
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                )
                login(request, user)
            elif action == 'SHADOW':
                shadow = Shadow.create_shadow(request, username=username)
                login(request, shadow.user)

            return HttpResponse()

