from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ibanproject import settings
from django.http import request, HttpResponse, HttpResponseRedirect
from ibanproject.GoogleOAuth.Google import GoogleOAuth
from django.contrib import messages
from django.db import transaction
from .common import *
from ibanmanage.models import *
from django.contrib.auth import login

# Create your views here.
class GoogleAuthentication():
    def google_login(request):
        """Initiate call to GoogleOAuth

        It redirects user to google auth url on success and to login page if error

        Arguments:
            request object -- request to add error messages and code.

        Returns:
            HttpResponse -- HttpResponse redirect url
        """
        # try:
        url = GoogleOAuth.google_redirect(settings,request)
        if url:
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.ERROR, 'Could not login through google, please contact site administrator.')
            return HttpResponseRedirect('{loginfailed}'.format(loginfailed = settings.LOGIN_FAILED_URL))
        # except Exception as e:
        #     return HttpResponseRedirect(settings.LOGIN_URL)

    def site_authentication(request):
        """Get google user data using google token

        It request googleOAuth using toke to get user profile details.
        Using these datils we can login user into system or redirect to login page.

        Arguments:
            request -- to show messages and get request data for request google call

        Returns:
            HttpResponse --  HttpResponse redirect
        """
        token_data = GoogleOAuth.google_authenticate(request,settings)
        google_profile = GoogleOAuth.get_google_profile(token_data,settings)
        if google_profile['email']:
            try:
                with transaction.atomic():
                    username,domainpart = google_profile['email'].split('@')
                    existing_user = User.objects.filter(username=username,email=google_profile['email'])
                    if existing_user.count() <= 0:
                        find_group = Group.objects.filter(name='Ibanadmin')
                        if not find_group:
                            group = create_group()
                        else:
                            group = Group.objects.get(name='Ibanadmin')
                        user = User.objects.create_user(first_name = google_profile['given_name'], last_name = google_profile['family_name'], username=username, email=google_profile['email'], password=username,is_active=False)
                        user.groups.add(group)
                        messages.success(request, 'Superadmin will shortly activate you, after which you can login in the system.')
                        return HttpResponseRedirect(settings.LOGIN_URL)
                    else:
                        #login user into system
                        user = User.objects.get(username=username,email=google_profile['email'])
                        if user.is_active:
                            login(request, user)
                            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
                        else:
                            messages.error(request, 'Your Account Is Not Yet Activated.')
                            return HttpResponseRedirect(settings.LOGIN_URL)
            except:
                messages.error(request, 'Invalid Response From Google')
                return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            messages.error(request, 'Invalid Response From Google')
            return HttpResponseRedirect(settings.LOGIN_URL)

def loginfailed(request):
	return render(request, 'loginfailed.html')

class BaseViews():
    @login_required(login_url=settings.LOGIN_URL)
    def dashboard(request):
        return render(request,"dashboard.html")