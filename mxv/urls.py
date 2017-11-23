"""mxv URL Configuration

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
