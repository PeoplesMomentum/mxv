from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^activate/(?P<activation_key>[a-zA-Z0-9]+)/$', views.activate, name='activate'),
]