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
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from ibanuserapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),    
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
    url(r'^authlogin/$', views.GoogleAuth.login, name='usergoogleauth'),
    url(r'^auth/complete/google-oauth2/$', views.GoogleAuth.auth, name='usergoogleauthresponse'), 
    url(r'^dashboard/', views.Home.as_view(), name='home'),
    url(r'^add/', views.Create.as_view(), name='add'),
    url(r'^update/(?P<pk>\d+)/$', views.Update.as_view(), name='update'),
    url(r'^delete/(?P<pk>\d+)/$', views.Delete.as_view(), name='delete'),    
]
