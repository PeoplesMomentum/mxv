from django.conf.urls import url

from review import views

app_name = 'review'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^track/(?P<pk>\d+)/$', views.track, name = 'track'),
    url(r'^theme/(?P<pk>\d+)/$', views.theme, name = 'theme'),
    url(r'^theme/(?P<pk>\d+)/new_proposal/$', views.new_proposal, name = 'new_proposal'),
    url(r'^proposal/(?P<pk>\d+)/$', views.proposal, name = 'proposal'),
]