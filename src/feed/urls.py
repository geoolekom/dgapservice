from django.conf.urls import url, include
from feed.views import *
from django.contrib.auth.decorators import login_required, permission_required

# app_name = 'feed'
urlpatterns = [
	url(r'^(?P<pk>\d+)', PostDetail.as_view(), name="detail"),
	url(r'^rate/(?P<pk>\d+)', PostRateView.as_view(), name="rate"),
	url(r'^ratings', ListRateView.as_view(), name="ratings"),
	url(r'^$', Feed.as_view(), name="feed"),
	url(r'comments/(?P<pk>\d+)', DetailCommentView.as_view(), name="comment-detail"),
	url(r'comments/edit/(?P<pk>\d+)', EditComment.as_view(), name="comment-edit"),
	url(r'comments/add', AddComment.as_view(), name="comment-add"),
	url(r'comments/delete', DeleteComment.as_view(), name="comment-delete"),
	url(r'posts/edit/(?P<pk>\d+)', EditPost.as_view(), name="post-edit"),
	url(r'posts/add', permission_required('post.add')(AddPost.as_view()), name="post-add"),
	url(r'posts/delete', DeletePost.as_view(), name="post-delete"),
]