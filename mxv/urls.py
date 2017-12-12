from django.conf.urls import include, url
from django.contrib import admin
from . import views
from users import views as users_views

# this all needs tidying up: 
#  - admin urls (edit, send and import) should be in an urls.py
#  - users and members should all be under /members/


urlpatterns = [
    # landing page
    url(r'^$', views.index, name='index'),
    # authentication and users
    url(r'^members/', include('django.contrib.auth.urls')),
    url(r'^users/', include('users.urls')),
    # admin
    url(r'^admin/edit_member_activation_email/$', users_views.edit_member_activation_email, name = 'edit_member_activation_email'),
    url(r'^admin/send_member_activation_emails/$', users_views.send_member_activation_emails, name = 'send_member_activation_emails'),
    url(r'^admin/import_member_names_and_email_addresses/$', users_views.import_member_names_and_email_addresses, name = 'import_member_names_and_email_addresses'),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/', admin.site.urls),
    # democracy review
    url(r'^democracy_review/', include('review.urls')),
]
