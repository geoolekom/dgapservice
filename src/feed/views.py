from feed.models import Post as myPost
from feed.models import RatedPost, Comment
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import AddCommentForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


class Feed(ListView):
	template_name = 'feed/feed.html'

	def get_queryset(self):
		queryset = myPost.objects.all().order_by('-pub_time')

		if 'searchstr' in self.request.GET:
			searchstr = self.request.GET['searchstr']
			queryset = queryset.filter(entry__icontains=searchstr)
		elif 'sort' in self.request.GET:
			if self.request.GET['sort'] == '1':
				queryset = queryset.order_by('-pub_time')
			elif self.request.GET['sort'] == '2':
				queryset = queryset.order_by('-rating')
			else:
				pass
		else:
			pass

		return queryset


class Post(DetailView):
	template_name = 'feed/post.html'
	model = myPost
	add_comment_form = AddCommentForm()

	def get_context_data(self, **kwargs):
		parent = super(Post, self)
		context = parent.get_context_data(**kwargs)
		context['comments'] = self.get_object().comment_set.all()
		context['add_comment_form'] = self.add_comment_form
		return context

	def render_to_response(self, context, **response_kwargs):
		self.add_comment_form.author = self.request.user
		self.add_comment_form.post = self.get_object()
		self.add_comment_form.save()
		return super(Post, self).render_to_response(context, **response_kwargs)


class PostDetail(CreateView):
	template_name = 'feed/post.html'
	model = Comment
	form_class = AddCommentForm

	def dispatch(self, request, pk=None, *args, **kwargs):
		self.related_post = get_object_or_404(myPost, pk=pk)
		return super(PostDetail, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		parent = super(PostDetail, self)
		context = parent.get_context_data(**kwargs)
		context['post'] = self.related_post
		context['comments'] = self.related_post.comment_set.all()
		context['editing'] = 0
		return context
	
	def form_valid(self, form):
		comment = form.save(commit=False)
		if self.request.user.is_authenticated:
			comment.author = self.request.user
			comment.post = self.related_post
			comment.save()
		return redirect(self.request.META['HTTP_REFERER'])


class Delete(DeleteView):
	template_name = 'feed/post.html'
	model = Comment

	def get_object(self):
		obj = None
		if 'comment' in self.request.POST:
			pk = self.request.POST['comment']
			obj = Comment.objects.get(pk=pk, author=self.request.user)
		elif 'post' in self.request.POST:
			pk = self.request.POST['post']
			obj = myPost.objects.get(pk=pk, author=self.request.user)
		else:
			pass
		return obj

	def get_success_url(self):
		return self.request.META['HTTP_REFERER']


class UpdateComment(PostDetail):

	def dispatch(self, request, *args, **kwargs):

		self.related_comment = get_object_or_404(Comment, pk=request.POST['comment'], author=request.user)
		pk = self.related_comment.post.id
		return super(UpdateComment, self).dispatch(request, pk=pk, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(UpdateComment, self).get_context_data(pk=self.related_comment.post.id, **kwargs)
		pk = self.related_comment.id
		context['editing'] = int(pk)
		context['form'] = AddCommentForm({'entry': self.related_comment.entry})
		return context

	def form_valid(self, form):
		setattr(self.related_comment, 'entry', form.cleaned_data['entry'])
		self.related_comment.save()
		return redirect('/feed/' + str(self.related_comment.post.id))

class UpdatePost(PostDetail):
	pass


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