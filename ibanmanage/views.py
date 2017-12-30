from django.shortcuts import render, get_object_or_404
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
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ibanmanage import forms
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

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

class Dashboard(ListView):
    """Dashboard for system

    User will be redirected to this class after login and it will display listing of IBAN users
    """
    model = Ibandata
    template_name = 'dashboard.html'
    paginate_by = 5

    @method_decorator(login_required(login_url=settings.LOGIN_URL))
    def dispatch(self, *args, **kwargs):
        return super(Dashboard, self).dispatch(*args, **kwargs)

    #redirect to login page
    def get_queryset(self):
        queryset = Ibandata.objects.filter(created_by = self.request.user)
        return queryset

class IbandataCreate(CreateView):
    """Create IBAN Users

    Create view for IBAN users
    """
    model = Ibandata
    template_name = 'iban_data_create.html'
    form_class = forms.IbandataCreateForm
    @method_decorator(login_required(login_url=settings.LOGIN_URL))
    @method_decorator(permission_required("add_ibandata"))
    def dispatch(self, *args, **kwargs):
        return super(IbandataCreate, self).dispatch(*args, **kwargs)

    def form_invalid(self, form):
        return super(IbandataCreate, self).form_invalid(form)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Data Added Successfuly.')
        return super(IbandataCreate, self).form_valid(form)

class IbandataEdit(UpdateView):
    """Update IBAN Users

    Update view for IBAN users
    """
    model = Ibandata
    form_class = forms.IbandataCreateForm
    template_name = 'iban_data_create.html'
    success_url = reverse_lazy('dashboard')

    @method_decorator(login_required(login_url=settings.LOGIN_URL))
    @method_decorator(permission_required("change_ibandata"))
    def dispatch(self, *args, **kwargs):
        return super(IbandataEdit, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Data Updated Successfuly.')
        return super(IbandataEdit, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(Ibandata, pk=self.kwargs['pk'])
        if not user.created_by == self.request.user:
            raise PermissionDenied()
        return user

class IbandataDelete(DeleteView):
    """Delete IBAN Users

    Delete view for IBAN users
    """
    model = Ibandata
    template_name = 'ibanmanage/ibandata_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    success_message = "Data Deleted Successfuly."

    @method_decorator(login_required(login_url=settings.LOGIN_URL))
    @method_decorator(permission_required("delete_ibandata"))
    def dispatch(self, *args, **kwargs):
        return super(IbandataDelete, self).dispatch(*args, **kwargs)

    def post(self, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(IbandataDelete, self).post(*args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(IbandataDelete, self).get_object()
        if not obj.created_by == self.request.user:
            raise PermissionDenied()
        return obj

@login_required(login_url=settings.LOGIN_URL)
def ibanunique(request):
    iban = Ibandata.objects.values('id').filter(iban__iexact=request.POST.get('iban'))
    if(iban and 'existingibanid' in request.POST and request.POST.get('existingibanid') and request.POST.get('existingibanid') != ""):
        iban = iban.exclude(pk=int(request.POST.get('existingibanid')))
    if (not iban):
        return HttpResponse('true')
    else:
        return HttpResponse('false')

def server_error(request):
    return render(request, 'error_pages/500.html')
 
def not_found(request):
    return render(request, 'error_pages/404.html')
 
def permission_denied(request):
    return render(request, 'error_pages/403.html')
 
def bad_request(request):
    return render(request, 'error_pages/400.html')