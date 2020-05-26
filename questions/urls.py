from django.conf.urls import url
from questions import views

app_name = 'questions'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^question/(?P<pk>\d+)/$', views.answers, name = 'answers'),
    url(r'^vote/(?P<pk>\d+)/$', views.vote, name = 'vote'),
]
