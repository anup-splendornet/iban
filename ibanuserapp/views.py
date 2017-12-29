from django.shortcuts import render,redirect
from ibanproject import settings
from django.http import HttpResponseRedirect
from ibanproject.GoogleOAuth.Google import GoogleOAuth
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.generic import View
from django.contrib import messages


# Create your views here.
class GoogleAuth:	
    def authenticate_user(request, google_profile):
        """ 
	        This method is used to check user is exist or not
			if user is exist return user object
	        if user is not exist create with active status=false and return its object            
        """
        # check whether the user exist or not
        try:            
        	user = User.objects.get(email=google_profile['email'])
        except:
            user = None           
        # if user already exist
        if user:
            if user.is_active == False:
                messages.error(request, 'Your account is not active. Please contact administrator.')
                return False
            else:
                return user
        else:
            # if user doesn't exist then register user            
            username = google_profile['email'].split('@')
            user = User.objects.create_user(first_name = google_profile['given_name'], last_name = google_profile['family_name'], username=username[0], email=google_profile['email'], is_active=False, password=username[0])
            messages.error(request, 'Your account is not active. Please contact administrator.')
            return False
                
    def auth(request):
        """
        	This Method is used to authenticate user according to google profile information
        	Get google profile info and check with user's data        	
        """
        # Initiate call to google to get Authentication Token
        token_data = GoogleOAuth.google_authenticate(request,settings)

        # for getting the google profile data
        google_profile = GoogleOAuth.get_google_profile(token_data,settings)            

        # for getting or for checking the status of user
        user = GoogleAuth.authenticate_user(request, google_profile)   
        
        # if user does exist then login and redirect to home page
        if user:
            login(request,user)            
            return redirect('home')
        else:
            return redirect('login')

    def login(request):                                
        try:
            url = GoogleOAuth.google_redirect(settings,request)
            if url:
                return HttpResponseRedirect(url)
            else:
                return HttpResponseRedirect(settings.LOGIN_FAILED_URL)          
        except Exception as e:
            return HttpResponseRedirect(settings.LOGIN_URL)


class Home(View):
    def get(self, request, *args):
        return render(request, 'userapp/home.html', {})

