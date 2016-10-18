from django.conf.urls import url, include
from feed.views import *

urlpatterns = [
	url(r'^(?P<pk>\d+)', Post.as_view(), name="detail"),
	url(r'^rate/(?P<pk>\d+)', rate, name="rate"),
	url(r'^$', Feed.as_view(), name="feed"),
]