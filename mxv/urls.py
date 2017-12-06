from django.conf.urls import include, url
from django.contrib import admin
from . import views
from users.views import member_activation_email

urlpatterns = [
    # landing page
    url(r'^$', views.index, name='index'),
    # authentication and users
    url(r'^members/', include('django.contrib.auth.urls')),
    url(r'^users/', include('users.urls')),
    # admin
    url(r'^admin/member_activation_email/$', member_activation_email, name = 'member_activation_email'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', admin.site.urls),
    # democracy review
    url(r'^democracy_review/', include('review.urls')),
]
