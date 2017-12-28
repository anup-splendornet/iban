from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from ibanproject.GoogleOAuth.Google import GoogleOAuth
from ibanproject import settings
from django.contrib import messages

# Create your views here.
class SocialAuthentication:
    def get_user(request, google_profile):
        """
            This function is used to get the user.

            Args: google profile information is in the arguement or parameter of function through which the user is
            identified or create the user with this information.

            Return: returns the user object
        """
        # check whether the user exist or not
        try:
            user = User.objects.get(email=google_profile['email'])
        except:
            user = None
        # if user already exist
        if user:
            # then check whether it is active or not
            if user.is_active == True:
                return user
            else:
                messages.error(request, 'Your account is not active. Kindly contact administrator.')
                return False
        else:
            # if user doesn't exist then create user
            username = google_profile['email'].split('@')
            user = User.objects.create_user(first_name = google_profile['given_name'], last_name = google_profile['family_name'], username=username[0], email=google_profile['email'], is_active=False, password=username[0])
            messages.error(request, 'Your account is not active. Kindly contact administrator.')     
            return False

    def google_login(request):
        # Method to get URL, based on constants defined in setting file.
        try:
            url = GoogleOAuth.google_redirect(settings,request)
        except:
            url = None

        if url:
            return HttpResponseRedirect(url)
        else:
            return redirect('login')

    def site_authentication(request):
        # Initiate call to google to get Authentication Token
        token_data = GoogleOAuth.google_authenticate(request,settings)

        # for getting the google profile data
        google_profile = GoogleOAuth.get_google_profile(token_data,settings)

        # for getting or for checking the status of user
        user = SocialAuthentication.get_user(request, google_profile)

        # if user does exist then login and redirect to home page
        if user:
            login(request,user)
            return redirect('home')
        else:
            return redirect('login')


class Dashboard(TemplateView):
    # get the view of home page
    def get(self, request, *args):
        return render(request, self.template_name, {})
