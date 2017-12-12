from django.conf.urls import url

from . import views

app_name = 'usersadmin'
urlpatterns = [
    url('create_inactive_user/', views.create_inactive_user, name='create_inactive_user'),
    url(r'^edit_member_activation_email/$', views.edit_member_activation_email, name = 'edit_member_activation_email'),
    url(r'^send_member_activation_emails/$', views.send_member_activation_emails, name = 'send_member_activation_emails'),
    url(r'^import_member_names_and_email_addresses/$', views.import_member_names_and_email_addresses, name = 'import_member_names_and_email_addresses'),
]