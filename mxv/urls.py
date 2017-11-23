from django.conf.urls import include, url
from django.contrib import admin
from . import views
from users.views import member_activation

urlpatterns = [
    # landing page
    url(r'^$', views.index, name='index'),
    # authentication and users
    url(r'^members/', include('django.contrib.auth.urls')),
    url(r'^users/', include('users.urls')),
    # admin
    url(r'^admin/member_activation/$', member_activation, name = 'member_activation'),
    url(r'^admin/', admin.site.urls),
    # democracy review
    url(r'^democracy_review/', include('review.urls')),
]
