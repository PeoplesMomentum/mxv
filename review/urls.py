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
    url(r'^theme/(?P<pk>\d+)/proposal_submitted/$', views.proposal_submitted, name = 'proposal_submitted'),
    url(r'^proposal/(?P<pk>\d+)/$', views.proposal, name = 'proposal'),
    url(r'^proposal/(?P<pk>\d+)/edit/$', views.edit_proposal, name = 'edit_proposal'),
    url(r'^proposal/(?P<pk>\d+)/delete/$', views.delete_proposal, name = 'delete_proposal'),
    url(r'^proposal/(?P<pk>\d+)/moderate/$', views.moderate_proposal, name = 'moderate_proposal'),
    # amendments
    url(r'^proposal/(?P<pk>\d+)/new_amendment/$', views.new_amendment, name = 'new_amendment'),
    url(r'^amendment/(?P<pk>\d+)/$', views.amendment, name = 'amendment'),
    url(r'^amendment/(?P<pk>\d+)/edit/$', views.edit_amendment, name = 'edit_amendment'),
    url(r'^amendment/(?P<pk>\d+)/delete/$', views.delete_amendment, name = 'delete_amendment'),
    url(r'^amendment/(?P<pk>\d+)/moderate/$', views.moderate_amendment, name = 'moderate_amendment'),
    # comments
    url(r'^proposal/(?P<pk>\d+)/new_comment/$', views.new_comment, name = 'new_comment'),
    url(r'^comment/(?P<pk>\d+)/$', views.comment, name = 'comment'),
    url(r'^comment/(?P<pk>\d+)/moderate/$', views.moderate_comment, name = 'moderate_comment'),
    # support pages
    url(r'^help/$', views.help, name = 'help'),
    url(r'^rules/$', views.rules, name = 'rules'),
    url(r'^faq/$', views.faq, name = 'faq'),
    url(r'^moderation/$', views.moderation, name = 'moderation'),
    url(r'^guide/$', views.guide, name = 'guide'),
    #track voting
    url(r'^track_voting/(?P<pk>\d+)/$', views.track_voting, name = 'track_voting'),
]