from django.conf.urls import url
from consultations import views

app_name = 'consultations'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^consultation/(?P<pk>\d+)/$', views.consultation, name = 'consultation'),
    url(r'^thanks/(?P<pk>\d+)/$', views.thanks, name = 'thanks'),
]