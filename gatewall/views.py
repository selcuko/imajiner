from django.shortcuts import render
from django.core.exceptions import SuspiciousOperation
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from uuid import uuid4 as uuid
from django.contrib.auth.models import User
from identity.models import Shadow

class Auth(View):
    def get(self, request):
        return render(request, 'gatewall/auth.html', {})
    
    def post(self, request):
        p = request.POST
        print(p)
        try:
            action = p['action']

            if action == "shadow-check":
                fingerprint = p['fingerprint']
                shadow = Shadow.authenticate(fingerprint)
                if not shadow:
                    return JsonResponse({"found": False})
                return JsonResponse({
                    "found": True,
                    "username": shadow.user.username,
                })
                
            elif action == 'shadow-register':
                fingerprint = p['fingerprint']
                username = p.get('username', None)
                Shadow.create_shadow(request, fingerprint, username)
                return HttpResponse()

            else:
                raise SuspiciousOperation(f'Unknown action ID: {action}')

        except KeyError as ke:
                raise SuspiciousOperation(ke.args)


class LoginViews:

    class Login(View):

        def get(self, request):
            return render(request, 'gatewall/login.html')
        
        def post(self, request):
            action = request.POST.get('action', None)
            if action == 'LOGIN':
                username = request.POST.get('username', '')
                password = request.POST.get('password', '')
                user = authenticate(request, username=username, password=password)
                if user is None:
                    logout(request)
                    return HttpResponse('Siktir git yalancı', status=401)
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
            
            else:
                return HttpResponse(status=400)


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

