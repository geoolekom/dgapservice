from feed.models import Post as myPost
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic import RedirectView, View, DetailView, ListView
from feed.forms import *
from django.shortcuts import redirect, get_object_or_404, render, reverse
from django.http import HttpResponse, JsonResponse, Http404
from django.template.defaulttags import register
from django.db.models import Prefetch


@register.filter
def get_value_from_dict(dictionary, key):
	return dictionary.get(key)


class Feed(ListView):
	template_name = 'feed/feed.html'
	#   queryset = list(myPost.objects.all().order_by('-pub_time'))
	paginate_by = 4

	#   TODO: use javascript for search and filter
	def get_queryset(self):
		self.queryset = myPost.objects.all().order_by('-pub_time')

		if 'searchstr' in self.request.GET:
			searchstr = self.request.GET['searchstr']
			#   queryset = queryset.filter(entry__icontains=searchstr)
		else:
			searchstr = ''

		if 'sort' in self.request.GET:
			sort_type = self.request.GET['sort']
			if sort_type == '1':
				order_by = '-pub_time'
			elif sort_type == '2':
				order_by = '-rating'
			else:
				order_by = '-pub_time'
		else:
			order_by = '-pub_time'

		self.queryset = self.queryset.filter(entry__icontains=searchstr).order_by(order_by)
		return self.queryset

	def get_context_data(self, **kwargs):
		context = super(Feed, self).get_context_data(**kwargs)
		ratings = list(RatedPost.objects.filter(post__in=self.queryset).all())
		context['liked_by'] = dict()
		context['disliked_by'] = dict()

		for post in self.queryset:
			context['liked_by'][post.id] = [
				rating.user_id for rating in ratings
				if rating.mark == 1 and rating.post_id == post.id
				]
			context['disliked_by'][post.id] = [
				rating.user_id for rating in ratings
				if rating.mark == -1 and rating.post_id == post.id
				]

		return context


class PostDetail(DetailView):
	template_name = 'feed/post.html'
	post_id = None
	object = None
	model = Post

	def dispatch(self, request, pk=None, *args, **kwargs):
		self.post_id = int(pk)
		return super(PostDetail, self).dispatch(request, pk, *args, **kwargs)

	def get_object(self, queryset=None):
		self.object = Post.objects.filter(pk=self.post_id)\
			.prefetch_related('comment_set__author')\
			.prefetch_related('ratedpost_set').get()
		return self.object

	def get_context_data(self, **kwargs):
		parent = super(PostDetail, self)
		context = parent.get_context_data(**kwargs)
		context['post'] = self.object
		context['comments'] = self.object.comment_set.all()
		context['add_form'] = AddCommentForm()
		context['liked_by'] = dict()
		context['disliked_by'] = dict()

		ratings = self.object.ratedpost_set.all()
		context['liked_by'][self.object.id] = [
				rating.user_id for rating in ratings
				if rating.mark == 1 and rating.post_id == self.object.id
				]
		context['disliked_by'][self.object.id] = [
				rating.user_id for rating in ratings
				if rating.mark == -1 and rating.post_id == self.object.id
				]
		return context


class AddPost(CreateView):
	template_name = 'feed/post_form.html'
	model = myPost
	fields = ('title', 'entry',)

	def get_context_data(self, **kwargs):
		context = super(AddPost, self).get_context_data(**kwargs)
		context['editing_title'] = 'Новый пост'
		return context

	def form_valid(self, form):
		post = form.save(commit=False)
		post.author = self.request.user
		post.rating = 0
		post.save()
		return redirect(reverse('feed:detail', kwargs={"pk": post.pk}))


class DeletePost(DeleteView):
	template_name = 'feed/feed.html'
	model = Post

	def get_object(self, queryset=None):
		if 'id' in self.request.POST:
			feedpost = get_object_or_404(Post, pk=self.request.POST['id'], author=self.request.user)
			return feedpost
		else:
			raise Http404

	def delete(self, request, *args, **kwargs):
		super(DeletePost, self).delete(request, *args, **kwargs)
		return HttpResponse("OK")

	def get_success_url(self):
		return reverse('feed:feed')


class EditPost(UpdateView):
	template_name = 'feed/post_form.html'
	model = myPost
	form_class = AddPostForm

	def dispatch(self, request, pk=None, *args, **kwargs):
		self.object = get_object_or_404(myPost, author=request.user, pk=pk)
		return super(EditPost, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(EditPost, self).get_context_data(**kwargs)
		context['form'] = AddPostForm({'title': self.object.title, 'entry': self.object.entry})
		context['editing_title'] = self.object.title
		return context

	def get_object(self, queryset=None):
		return self.object

	def form_valid(self, form):
		if form.is_valid:
			post = form.save(commit=False)
			post.save()
			return redirect('/feed/' + str(self.object.id))
		else:
			return render(self.request, self.template_name, {'form': form})


class DetailCommentView(DetailView):
	model = Comment
	template_name = 'feed/comment.html'


class EditComment(UpdateView):
	template_name = "feed/comment_form.html"
	model = Comment
	form_class = AddCommentForm

	def get_object(self, queryset=None):
		comment = super(EditComment, self).get_object()
		if comment.author == self.request.user:
			return comment
		else:
			raise Http404

	def get(self, request, *args, **kwargs):
		self.form = AddCommentForm({'entry': self.get_object().entry})
		return super(EditComment, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		comment = self.get_object()
		if 'entry' in request.POST:
			entry = request.POST['entry']
			setattr(comment, 'entry', entry)
			comment.save()
			return HttpResponse(entry)
		else:
			raise Http404


class AddComment(CreateView):
	template_name = "feed/add_comment_form.html"
	model = Comment
	form_class = AddCommentForm

	def post(self, request, *args, **kwargs):
		if request.user.is_authenticated and 'entry' in request.POST and 'post_id' in request.POST:
			comment = Comment(
				author=request.user,
				entry=request.POST['entry'],
				post=get_object_or_404(Post, pk=request.POST['post_id'])
			)
			comment.save()
			return HttpResponse(comment.pk)
		else:
			raise Http404


class DeleteComment(DeleteView):
	model = Comment
	template_name = "feed/post.html"

	def get_object(self, queryset=None):
		if 'id' in self.request.POST:
			comment = get_object_or_404(Comment, pk=self.request.POST['id'], author=self.request.user)
			self.post_id = comment.post.id
			return comment
		else:
			raise Http404

	def delete(self, request, *args, **kwargs):
		super(DeleteComment, self).delete(request, *args, **kwargs)
		return HttpResponse("OK")

	def get_success_url(self):
		return reverse('feed:detail', kwargs={'pk': self.post_id})


class ListRateView(View):

	def get(self, request):
		ids = request.GET.get('ids', '')
		ids = ids.split(',')
		posts = dict(Post.objects.filter(id__in=ids).values_list('id', 'rating'))
		return JsonResponse(posts)


class PostRateView(View):

	def dispatch(self, request, pk=None, *args, **kwargs):
		self.feedpost = get_object_or_404(myPost, pk=pk)
		return super(PostRateView, self).dispatch(request, *args, **kwargs)

	def get(self, request):
		return HttpResponse(self.feedpost.rating)

	def post(self, request):
		user = request.user
		mark = int(request.POST['mark'])
		if abs(mark) == 1 and user.is_authenticated:
			RatedPost.objects.update_or_create(
				user=user,
				post=self.feedpost,
				defaults={'mark': mark}
			)
			self.feedpost.update_rating()
		return HttpResponse(self.feedpost.rating)


class JsonPosts(View):

	def get(self, request):
		if request.GET:
			post = get_object_or_404(Post, pk=request.GET['id'])
			post_dict = {'posts': [{
				'id': post.id,
				'title': post.title,
				'entry': post.entry,
				'author': post.author.username,
				'comments': [
					{
						'author': comment.author.username,
						'entry': comment.entry,
					} for comment in post.comment_set.all()],
			}]}
		else:
			post_dict = {"posts": [{
				'id': post.id,
				'title': post.title,
				'entry': post.entry,
				'author': post.author.username,
			} for post in Post.objects.all()]}
		return JsonResponse(post_dict)


