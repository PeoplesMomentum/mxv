from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url('create_inactive_user/', views.create_inactive_user, name='create_inactive_user'),
    url(r'^activate/(?P<activation_key>[a-zA-Z0-9]+)/$', views.activate, name='activate'),
]