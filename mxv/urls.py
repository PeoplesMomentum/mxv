from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # landing page
    url(r'^$', views.index, name='index'),
    
    # authentication and users
    url(r'^members/', include('users.urls')),
    
    # admin
    url(r'^admin/', include('users.adminurls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', admin.site.urls),
    
    # democracy review
    url(r'^democracy_review/', include('review.urls')),
]
