from django.shortcuts import render
from ibanproject.GoogleOAuth.Google import GoogleOAuth
from django.http import request, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from ibanproject import settings
from django.contrib.auth.models import User
from django.contrib.auth import login
# Create your views here.

class GoogleAuthViews():
    def get_google_token(request):
        try:
            url = GoogleOAuth.google_redirect(settings,request)
            if url:
                return HttpResponseRedirect(url)
            else:
                messages.add_message(request, messages.ERROR, 'Failed to login through google, please contact site admin.')
                return HttpResponseRedirect('{loginfailed}'.format(loginfailed = settings.LOGIN_FAILED_URL))
        except Exception as e:
            return HttpResponseRedirect(settings.LOGIN_URL)
    def get_google_profile_data(request):
        token_data = GoogleOAuth.google_authenticate(request,settings)
        google_user_profile = GoogleOAuth.get_google_profile(token_data,settings)
        try:
            if google_user_profile['email']:
                username,domain = google_user_profile['email'].split('@')
                user_exist = User.objects.filter(username=username,email=google_user_profile['email'])
                if user_exist.count() <= 0:
                    user = User.objects.create_user(first_name = google_user_profile['given_name'], last_name = google_user_profile['family_name'], username=username, email=google_user_profile['email'], password=username,is_active=False)
                    messages.success(request, 'Admin will shortly activate your account, after which you can login in the system.')
                    return HttpResponseRedirect(settings.LOGIN_URL)
                else:
                    #Existing user login
                    user = User.objects.get(username=username,email=google_user_profile['email'])
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
                    else:
                        messages.error(request, 'Account is not yet activated.')
                        return HttpResponseRedirect(settings.LOGIN_URL)
            else:
                messages.error(request, 'Invalid response')
                return HttpResponseRedirect(settings.LOGIN_URL)
        except:
                messages.error(request, 'Invalid response')
                return HttpResponseRedirect(settings.LOGIN_URL)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

class GeneralViews():
    def dashboard(request):
        return render(request,"dashboard.html")
