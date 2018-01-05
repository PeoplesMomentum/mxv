from django.conf.urls import url

from review import views

app_name = 'review'
urlpatterns = [
    url(r'^$', views.index, name='index')
]