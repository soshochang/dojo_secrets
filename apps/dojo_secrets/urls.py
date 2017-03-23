from django.conf.urls import url
from . import views
urlpatterns = [
  url(r'^$', views.index),
  url(r'^register$', views.register),
  url(r'^login$', views.login),
  url(r'^logout$', views.logout),
  url(r'^success/(?P<id>\d+)$', views.success),
  
  url(r'^home$', views.home),
  url(r'^most_popular$', views.most_popular),
  url(r'^create_secret$', views.create_secret),
  url(r'^delete_secret$', views.delete_secret),
  url(r'^create_like$', views.create_like),
]