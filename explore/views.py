from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from notebook.models import Narrative
from django.conf import settings
from django.http import HttpResponsePermanentRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from .models import Feedback as FeedbackModel


def red(request):
    return HttpResponsePermanentRedirect(f'https://{settings.PRIMARY_HOST}')

class Home(View):
    template_name = 'landing.html'
    def get(self, request, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request):
        return HttpResponse(status=403)


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


class Feedback(View):
    def post(self, request):
        data = request.POST
        try:
            user_id = data.get('user-id', None)
            if not isinstance(user_id, int):
                try: user_id = int(user_id)
                except: user_id = None
            ua = data['ua']
            session_key = data['session-key']
            location = data['location']
            referrer = data.get('referrer', None)
            message = data['message']
            user = User.objects.filter(id=user_id).first() if user_id else None
            session = Session.objects.filter(session_key=session_key).first() if session_key else None
            print('USER', user)
            feedback = FeedbackModel.objects.create(
                user=user,
                session=session,
                ua=ua,
                location=location,
                referrer=referrer,
                message=message,
            )

        except KeyError as ke:
            print(repr(ke))
            return HttpResponse(ke, status=400)
        
        return HttpResponse()