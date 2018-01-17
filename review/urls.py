from django.conf.urls import url

from review import views

app_name = 'review'
urlpatterns = [
    # index
    url(r'^$', views.index, name='index'),
    
    #tracks
    url(r'^track/(?P<pk>\d+)/$', views.track, name = 'track'),
    
    # themes
    url(r'^theme/(?P<pk>\d+)/$', views.theme, name = 'theme'),
    
    # proposals
    url(r'^theme/(?P<pk>\d+)/new_proposal/$', views.new_proposal, name = 'new_proposal'),
    url(r'^proposal/(?P<pk>\d+)/$', views.proposal, name = 'proposal'),
    url(r'^proposal/(?P<pk>\d+)/edit/$', views.edit_proposal, name = 'edit_proposal'),
    url(r'^proposal/(?P<pk>\d+)/delete/$', views.delete_proposal, name = 'delete_proposal'),
    
    # amendments
    url(r'^proposal/(?P<pk>\d+)/new_amendment/$', views.new_amendment, name = 'new_amendment'),
    url(r'^amendment/(?P<pk>\d+)/$', views.amendment, name = 'amendment'),
    url(r'^amendment/(?P<pk>\d+)/edit/$', views.edit_amendment, name = 'edit_amendment'),
    url(r'^amendment/(?P<pk>\d+)/delete/$', views.delete_amendment, name = 'delete_amendment'),
]