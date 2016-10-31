from django.conf.urls import url, include
from feed.views import *
from django.contrib.auth.decorators import login_required, permission_required

# app_name = 'feed'
urlpatterns = [
	url(r'^(?P<pk>\d+)', PostDetail.as_view(), name="detail"),
	url(r'^rate/(?P<pk>\d+)', rate, name="rate"),
	url(r'^$', Feed.as_view(), name="feed"),
	url(r'delete', Delete.as_view(), name="delete"),
	url(r'edit-comment', EditComment.as_view(), name="edit"),
	url(r'edit-post', EditPost.as_view(), name="edit"),
	url(r'add', permission_required('post.add')(AddPost.as_view()), name="add_post"),
]