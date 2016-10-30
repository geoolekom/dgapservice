from django.conf.urls import url, include
from feed.views import *

# app_name = 'feed'
urlpatterns = [
	url(r'^(?P<pk>\d+)', PostDetail.as_view(), name="detail"),
	url(r'^rate/(?P<pk>\d+)', rate, name="rate"),
	url(r'^$', Feed.as_view(), name="feed"),
	url(r'delete', Delete.as_view(), name="delete"),
	url(r'edit', UpdateComment.as_view(), name="edit"),
]