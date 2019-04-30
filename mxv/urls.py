from django.conf.urls import include, url
from django.contrib import admin
from . import views
from . import forms
from django.contrib.auth import views as auth_views

urlpatterns = [
    # landing page
    url(r'^$', views.index, name='index'),
    
    # activation and authentication
    url(r'^members/', include('members.urls')),
    url(r'^members/password_reset/$', views.ExtraContextPasswordResetView.as_view(form_class = forms.ActivationEmailPasswordResetForm), name='password_reset'),
    url(r'^members/login/$', auth_views.LoginView.as_view(form_class = forms.ActivationEmailAuthenticationForm), name='login'),
    url(r'^members/', include('django.contrib.auth.urls')),
    
    # admin
    url(r'^admin/', include('members.adminurls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
    
    # democracy review
    url(r'^review/', include('review.urls')),
    
    # error testing
    url(r'^error/$', views.error, name='error'),
    
    # GDPR
    url(r'^reconsent/$', views.reconsent, name='reconsent'),
    url(r'^reconsent_complete/$', views.reconsent_complete, name='reconsent_complete'),
    
    # voting intentions
    url(r'^voting_intentions/', include('voting_intentions.urls')),
    
    # consultations
    url(r'^consultations/', include('consultations.urls')),
    
    # task queueing
    url(r'^django-rq/', include('django_rq.urls')),
]