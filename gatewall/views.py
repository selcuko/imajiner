from django.shortcuts import render
from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from uuid import uuid4 as uuid
from django.contrib.auth.models import User
from identity.models import Shadow
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language_from_request
import time

class Auth(View):
    def get(self, request):
        i = request.GET.get('informative', None) is not None
        print('INFO', i, request.GET)
        return render(request, 'gatewall/gatewall.html', {
            'user': request.user,
            'informative': i,
            'doc': {
                'title': _('Authorization'),
                'author': _('Imajiner Gatewall'),
                'description': _('You need to be authenticated in order to write here.'),
            }
            })
    
    def post(self, request):
        time.sleep(1)
        p = request.POST
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
            
            elif action == 'username-availability':
                username = p['username']
                return JsonResponse({'available': not User.objects.filter(username=username).exists()})
                
            elif action == 'shadow-register':
                fingerprint = p['fingerprint']
                username = p.get('username', None)
                shadow = Shadow.create_shadow(request, fingerprint, username)
                login(request, shadow.user)
                user = shadow.user
                request_language = get_language_from_request(request)
                request_language_path = get_language_from_request(request, check_path=True)
                print(request_language, request_language_path)
                if request_language:
                    user.profile.languages += [request_language]
                if request_language_path != request_language and request_language_path:
                    user.profile.languages += [request_language_path]
                return JsonResponse({'username': username})

            elif action == 'shadow-login':
                fingerprint = p['fingerprint']
                username = p.get('username', None)
                shadow = Shadow.authenticate(fingerprint)
                if not shadow:
                    return JsonResponse(status=403)
                login(request, shadow.user)
                return JsonResponse({})
            
            elif action == 'author-register':
                username = p['username']
                password = p['password']
                try:
                    user = User.objects.create_user(username=username, password=password)
                    login(request, user)
                except IntegrityError:
                    return JsonResponse({'error': True})
                
                request_language = get_language_from_request(request)
                request_language_path = get_language_from_request(request, check_path=True)
                print(request_language, request_language_path)
                if request_language:
                    user.profile.languages += [request_language]
                if request_language_path != request_language and request_language_path:
                    user.profile.languages += [request_language_path]
                user.profile.save()
                return JsonResponse({'error': False})
            
            elif action == 'author-login':
                username = p['username']
                password = p['password']
                user = authenticate(username=username, password=password)
                if not user:
                    return JsonResponse(status=403)
                login(request, user)
                return JsonResponse({})
            
            elif action == 'author-check':
                username = p['username']
                if User.objects.filter(username=username).exists():
                    return JsonResponse(status=400)
                else:
                    return JsonResponse(status=200)
            
            elif action == 'logout':
                if not request.user.is_authenticated:
                    raise SuspiciousOperation
                logout(request)
                return JsonResponse({})

            else:
                error = f'Unknown action ID: {action}'
                print(error)
                return JsonResponse(status=400)

        except KeyError as ke:
            print("KeyError on auth", ke.args, ke.kwargs)
            return JsonResponse(form.errors, status=400)


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return HttpResponse('Y O U R E  O U T')

