from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # landing page
    url(r'^$', views.index, name='index'),
    
    # activation and authentication
    url(r'^members/', include('members.urls')),
    
    # admin
    url(r'^admin/', include('members.adminurls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', admin.site.urls),
    
    # democracy review
    url(r'^democracy_review/', include('review.urls')),
]
