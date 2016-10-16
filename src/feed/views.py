from django.shortcuts import render
from feed.models import Post
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

class Feed(ListView):
	template_name = 'feed/feed.html'
	queryset = Post.objects.all().order_by('-pub_time')

class Post(DetailView):
	template_name = 'feed/post.html'
	model = Post