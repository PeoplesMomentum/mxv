from django.conf.urls import url
from voting_intentions import views

app_name = 'voting_intentions'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]