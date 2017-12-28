from django.shortcuts import render
from django.http import request, HttpResponse, HttpResponseRedirect
from ibanproject import settings
from django.contrib import messages
from ibanproject.messagestext import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.

class AuthView():

    def login(request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            return render(request, 'registration/login.html')

    def logout(request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    @login_required(login_url=settings.LOGIN_URL) #Login check
    def dashboard(request):
        return render(request, 'dashboard.html')

def server_error(request):
    return render(request, 'errors/500.html')

def not_found(request):
    return render(request, 'errors/404.html')

def permission_denied(request):
    return render(request, 'errors/403.html')

def bad_request(request):
    return render(request, 'errors/400.html')