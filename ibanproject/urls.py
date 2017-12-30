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
from django.contrib.auth import views
from ibanmanage.views import *
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.login, name='login'),
    url(r'^login/$', views.login, kwargs={'redirect_authenticated_user': True}, name='login'),
    url(r'^logout/$', views.logout,{'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^authlogin/$', GoogleAuthentication.google_login, name='authlogin'),
    url(r'^auth/complete/google-oauth2/$', GoogleAuthentication.site_authentication, name='googleauthenticate'),
    url(r'^loginfailed/$', loginfailed, name='loginfailed'),
    url(r'^dashboard/$', Dashboard.as_view(),{},  name='dashboard'),
    url(r'^addibandata/$', IbandataCreate.as_view(model=Ibandata, success_url='/dashboard/'), {},  name='addibandata'),
    url(r'^editibandata/(?P<pk>\d+)/$', IbandataEdit.as_view(model=Ibandata, success_url='/dashboard/'), {},  name='editibandata'),
    url(r'^deleteibandata/(?P<pk>\d+)/$', IbandataDelete.as_view(), name='deleteibandata'),
    url(r'^ibanunique/$', ibanunique, name='ibanunique'),
]
handler400 = 'ibanmanage.views.bad_request'
handler403 = 'ibanmanage.views.permission_denied'
handler404 = 'ibanmanage.views.not_found'
handler500 = 'ibanmanage.views.server_error'