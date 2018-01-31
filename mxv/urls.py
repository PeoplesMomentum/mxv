from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # landing page
    url(r'^$', views.index, name='index'),
    
    # activation and authentication
    url(r'^members/', include('members.urls')),
    url(r'^members/password_reset/$', views.ExtraContextPasswordResetView.as_view(), name='password_reset'),
    url(r'^members/', include('django.contrib.auth.urls')),
    
    # admin
    url(r'^admin/', include('members.adminurls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', admin.site.urls),
    
    # democracy review
    url(r'^review/', include('review.urls')),
    
    # error testing
    url(r'^error/$', views.error, name='error'),
]
