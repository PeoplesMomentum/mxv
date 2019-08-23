from django.conf.urls import url
from . import views

app_name = 'members'
urlpatterns = [
    # called by the join page
    url(r'^create_inactive_member/$', views.create_inactive_member, name='create_inactive_member'), 
    
    # activation
    url(r'^request_activation_email/$', views.request_activation_email, name='request_activation_email'), 
    url(r'^activate/(?P<activation_key>[a-zA-Z0-9]+)/$', views.activate, name='activate'),  
    
    # profile
    url(r'^profile/$', views.profile, name='profile'), 
    url(r'^change_login_email/$', views.change_login_email, name='change_login_email'), 
    url(r'^login_email_verification_sent/$', views.login_email_verification_sent, name='login_email_verification_sent'), 
    url(r'^verify_login_email/(?P<login_email_verification_key>[a-zA-Z0-9]+)/$', views.verify_login_email, name='verify_login_email'),
    
    # update details campaign
    url(r'^update_details/(?P<page>\d+)/$', views.update_details, name='update_details'), 
]

