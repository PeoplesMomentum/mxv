from django.conf.urls import url, include
from . import views

app_name = 'users'
urlpatterns = [
    # user activation
    url(r'^activate/(?P<activation_key>[a-zA-Z0-9]+)/$', views.activate, name='activate'),
    
    # authentication URLs included here instead of in mxv/urls.py so that they have the app name 'users'
    url(r'^', include('django.contrib.auth.urls')),
]