"""ibanproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf.urls import handler404, handler500
from ibanuser import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', auth_views.login, name='loginuser'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
    url(r'^authlogin/$', views.SocialAuthentication.google_login, name='authlogin'),
    url(r'^auth/complete/google-oauth2/$', views.SocialAuthentication.site_authentication, name='googleauthenticate'),
    url(r'^dashboard/', login_required(views.Dashboard.as_view(template_name='ibanuser/dashboard.html')), name='home'),
    url(r'^adduser/$', login_required(views.CreateUser.as_view(template_name='ibanuser/ibaninfo.html')), name='adduser'),
    url(r'^edituser/(?P<pk>\d+)/$', login_required(views.EditUser.as_view(template_name='ibanuser/ibaninfo.html')), name='edituser'),
    url(r'^deleteuser/(?P<pk>\d+)/$', login_required(views.DeleteUser.as_view()), name='deleteuser'),
]

handler404 = views.Error.as_view()
handler500 = views.Error.as_view()
