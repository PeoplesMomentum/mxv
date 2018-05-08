from django.conf.urls import url

from . import views

app_name = 'membersadmin'
urlpatterns = [
    url('create_inactive_member/', views.create_inactive_member, name='create_inactive_member'),
    url(r'^send_member_activation_emails/$', views.send_member_activation_emails, name = 'send_member_activation_emails'),
]