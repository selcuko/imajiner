from django.shortcuts import render

def handle404(request):
    return render(request, '404.html')