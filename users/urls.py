from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url('create_inactive_user/', views.create_inactive_user, name='create_inactive_user')
]