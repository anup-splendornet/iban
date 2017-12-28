from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ibanproject import settings
from django.http import request, HttpResponse, HttpResponseRedirect


# Create your views here.
class BaseViews():
    @method_decorator(login_required(login_url=settings.LOGIN_URL))
    def dashboard(request):
        return render(request,"dashboard.html")