from django.shortcuts import render
from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from uuid import uuid4 as uuid
from django.contrib.auth.models import User
from identity.models import Shadow

class Auth(View):
    def get(self, request):
        return render(request, 'gatewall/auth.html', {'user':request.user})
    
    def post(self, request):
        p = request.POST
        print(p)
        try:
            action = p['action']

            if action == "shadow-check":
                fingerprint = p['fingerprint']
                shadow = Shadow.authenticate(fingerprint)
                print('FOUND:', shadow)
                if not shadow:
                    return JsonResponse({"found": False})
                return JsonResponse({
                    "found": True,
                    "username": shadow.user.username,
                })
                
            elif action == 'shadow-register':
                fingerprint = p['fingerprint']
                username = p.get('username', None)
                shadow = Shadow.create_shadow(request, fingerprint, username)
                login(request, shadow.user)
                return HttpResponse()

            elif action == 'shadow-login':
                fingerprint = p['fingerprint']
                username = p.get('username', None)
                shadow = Shadow.authenticate(fingerprint)
                if not shadow:
                    return HttpResponse(status=403)
                login(request, shadow.user)
                return HttpResponse()
            
            elif action == 'author-register':
                username = p['username']
                password = p['password']
                try:
                    user = User.objects.create_user(username=username, password=password)
                    login(request, user)
                except IntegrityError:
                    return JsonResponse({'error': True})
                return JsonResponse({'error': False})
            
            elif action == 'author-login':
                username = p['username']
                password = p['password']
                user = authenticate(username=username, password=password)
                if not user:
                    return HttpResponse(status=403)
                login(request, user)
                return HttpResponse()
            
            elif action == 'author-check':
                username = p['username']
                if User.objects.filter(username=username).exists():
                    return HttpResponse(status=422)
                else:
                    return HttpResponse(status=200)
            
            elif action == 'logout':
                if not request.user.is_authenticated:
                    raise SuspiciousOperation('Girmediğin kapıdan çıkamazsın.')
                logout(request)
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

