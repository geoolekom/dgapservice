from django.conf.urls import url, include
from feed.views import *

# app_name = 'feed'
urlpatterns = [
	url(r'^(?P<pk>\d+)', Post.as_view(), name="detail"),
	url(r'^rate/(?P<pk>\d+)', rate, name="rate"),
	url(r'^$', Feed.as_view(), name="feed"),
]