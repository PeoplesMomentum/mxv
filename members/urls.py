from django.conf.urls import url
from . import views

app_name = 'members'
urlpatterns = [
    url(r'^create_inactive_member/$', views.create_inactive_member, name='create_inactive_member'), 
    url(r'^request_activation_email/$', views.request_activation_email, name='request_activation_email'), 
    url(r'^activate/(?P<activation_key>[a-zA-Z0-9]+)/$', views.activate, name='activate'),  
]

