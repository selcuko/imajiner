from django.shortcuts import render

def console(request):
    return render(request, 'console/overview.html', {})
