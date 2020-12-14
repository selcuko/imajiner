from django.shortcuts import render, redirect
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
import logging
from .forms import UserForm, ShadowForm

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Auth(View):
    def get(self, request):

        return render(request, 'gatewall/gatewall.html', {
            'user': request.user,
            'informative': request.GET.get('informative') ,
            'forms': {
                'author': UserForm(),
                'shadow': ShadowForm(),
            },
            'doc': {
                'title': _('Authorization'),
                'author': _('Imajiner Gatewall'),
                'description': _('You need to be authenticated in order to write here.'),
            }})
    

    def post(self, request):
        try:
            action = request.POST['action']
            
            if action == "shadow-check":
                shadow = Shadow.authenticate(request.POST['fingerprint'])
                if not shadow:
                    return JsonResponse({'found': False})
                return JsonResponse({
                    'found': True,
                    'username': shadow.user.username,
                })
            
            elif action == 'username-availability':
                taken = User.objects.filter(username=request.POST['username']).exists()
                return JsonResponse({'available': not taken})
                
            elif action == 'shadow-register':
                
                try:
                    shadow = Shadow.create_shadow(
                        request, 
                        request.POST['fingerprint'], 
                        request.POST.get('username', '')
                        )
                except IntegrityError:
                    return JsonResponse({
                        'authenticated': False
                    }, status=400)

                login(request, shadow.user)
                lang1 = get_language_from_request(request)
                lang2 = get_language_from_request(request, check_path=True)
                if lang1:
                    shadow.user.profile.languages += [lang1]
                if lang2 != lang1 and lang2:
                    shadow.user.profile.languages += [lang2]
                shadow.user.profile.save()
                return JsonResponse({
                    'username': shadow.user.username,
                    'authenticated': True})

            elif action == 'shadow-login':
                fingerprint = request.POST['fingerprint']
                shadow = Shadow.authenticate(fingerprint)
                if not shadow:
                    return JsonResponse({
                        'authenticated': False
                    }, status=403)
                else:
                    login(request, shadow.user)
                    return JsonResponse({
                        'authenticated': True
                    })
            
            elif action == 'author-register':
                form = UserForm(request.POST)
                if not form.is_valid():
                    JsonResponse({
                        'authenticated': False
                    }, status=400)
                try:
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'], 
                        password=form.cleaned_data['password'])
                    login(request, user)
                except IntegrityError:
                    return JsonResponse({'authenticated': False}, status=400)
                
                lang0 = get_language_from_request(request)
                lang1 = get_language_from_request(request, check_path=True)
                if lang0:
                    user.profile.languages += [lang0]
                if lang0 != lang1 and lang1:
                    user.profile.languages += [lang1]
                user.profile.save()
                return JsonResponse({'authenticated': True})
            
            elif action == 'author-login':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if not user:
                    return JsonResponse({'authenticated': False})
                else:
                    login(request, user)
                    return JsonResponse({'authenticated': True})
            
            elif action == 'logout':
                if not request.user.is_authenticated:
                    raise SuspiciousOperation
                logout(request)
                return JsonResponse({})

            else:
                return JsonResponse({}, status=400)

        except KeyError as ke:
            logging.error(f'KeyError on AuthView: {ke!r}')
            return JsonResponse({}, status=400)


class Logout(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect('gatewall:auth')

