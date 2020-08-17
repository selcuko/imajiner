from django.shortcuts import render, HttpResponse

def mastermind(request):
    return render(request, 'info/mastermind.html')


