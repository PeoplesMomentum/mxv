from django.conf.urls import url

from . import views

app_name = 'membersadmin'
urlpatterns = [
    url('create_inactive_member/', views.create_inactive_member, name='create_inactive_member'),
    url(r'^edit_member_activation_email/$', views.edit_member_activation_email, name = 'edit_member_activation_email'),
    url(r'^send_member_activation_emails/$', views.send_member_activation_emails, name = 'send_member_activation_emails'),
    url(r'^import_member_names_and_email_addresses/$', views.import_member_names_and_email_addresses, name = 'import_member_names_and_email_addresses'),
]