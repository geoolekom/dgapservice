from django.shortcuts import render
from feed.models import Post as myPost
from feed.models import RatedPost
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

class Feed(ListView):
	template_name = 'feed/feed.html'
	queryset = myPost.objects.all().order_by('-pub_time')

class Post(DetailView):
	template_name = 'feed/post.html'
	model = myPost

def rate(request, pk):
	post = myPost.objects.all().get(pk=pk)
	mark = int(request.POST['mark'])
	user = request.user
	
	try:
		rated = RatedPost.objects.all().get(user=user, post=post)
		post.changeRating(-rated.mark)
	except:
		rated = RatedPost(user=user, post=post)

	post.changeRating(mark)
	rated.mark = mark
	rated.save()

	return HttpResponseRedirect(request.META['HTTP_REFERER'])