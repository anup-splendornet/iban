from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Permission
from django.views.generic import View, TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from ibanproject.GoogleOAuth.Google import GoogleOAuth
from ibanproject import settings
from django.contrib import messages
from .models import IbanInfo
from .forms import IbanInfoForm

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

class Dashboard(ListView):
    # home page or dashboard
    model = IbanInfo
    context_object_name = 'userdetails'
    # queryset for the home page or dashboard
    def get_queryset(self):
        # if the user is superuser
        if self.request.user.is_authenticated():
            return IbanInfo.objects.filter(owner=self.request.user)
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['ibanusers'] = self.get_queryset()
        return context


class CreateUser(CreateView):
    # iban user creation functions
    model = IbanInfo
    form_class = IbanInfoForm
    success_url = reverse_lazy('home')

    # get the form for saving the data
    def get(self, request, *args):
        try:
            ibanadmin = request.user.groups.values_list('name',flat=True)
        except:
            ibanadmin = None
        # if the loggedin user doesn't have permission to be an admin then show error message      
        if 'ibanadmin' not in ibanadmin:
            messages.error(self.request, 'You are not authorized as an IBAN Admin.')
        else:
            permission_list = Permission.objects.values_list("codename",flat=True).filter(group__user=request.user)
            if 'add_ibaninfo' not in permission_list:
                messages.error(self.request, 'You are not authorized to add any information.')

        return render(request, self.template_name, {'form': self.form_class})

    # saving the form data for ibanusers
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateUser, self).form_valid(form)



class EditUser(UpdateView):
    # update functionality
    model = IbanInfo
    form_class = IbanInfoForm
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(EditUser, self).get_context_data(**kwargs)
        context['update'] = True
        return context

    # get the ibanuser object for update or edit
    def get_object(self, *args, **kwargs):
        ibanuser = get_object_or_404(IbanInfo, pk=self.kwargs['pk'])

        # if the user is not superuser and the loggedin user is not the owner of ibanuser then show error message
        permission_list = Permission.objects.values_list("codename",flat=True).filter(group__user=self.request.user)        
        if self.request.user != ibanuser.owner or 'change_ibaninfo' not in permission_list:                        
            messages.error(self.request, 'You are not authorized to change this information.')
            return None
        else:
            return ibanuser

class DeleteUser(DeleteView):
    # delete functionality
    model = IbanInfo
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(DeleteUser, self).get_context_data(**kwargs)
        context['delete'] = True
        return context

    # get the ibanuser object for deletion
    def get_object(self, queryset=None):
        ibanuser = super(DeleteUser, self).get_object()

        # if the user is not superuser and the loggedin user is not the owner of ibanuser then show error message
        permission_list = Permission.objects.values_list("codename",flat=True).filter(group__user=self.request.user)

        if  self.request.user != ibanuser.owner or 'delete_ibaninfo' not in permission_list:                        
            messages.error(self.request, 'You are not authorized to delete this information.')
            return None
        else:
            return ibanuser

class Error(View):
    # error page functions
    def get(self, request, *args):
        return render(request, 'error_all.html', {})
