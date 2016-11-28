from feed.models import Post as myPost
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import RedirectView, View
from .forms import *
from django.shortcuts import redirect, get_object_or_404, render, reverse
from django.http import HttpResponse, JsonResponse
import json


class Feed(ListView):
	template_name = 'feed/feed.html'

	def get_queryset(self):
		queryset = myPost.objects.all().order_by('-pub_time')

		if 'searchstr' in self.request.GET:
			searchstr = self.request.GET['searchstr']
			queryset = queryset.filter(entry__icontains=searchstr)
		if 'sort' in self.request.GET:
			if self.request.GET['sort'] == '1':
				queryset = queryset.order_by('-pub_time')
			elif self.request.GET['sort'] == '2':
				queryset = queryset.order_by('-rating')
			else:
				pass
		return queryset


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
		return redirect(reverse("feed:detail", kwargs={"pk": self.related_post.pk}))


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


class Delete(DeleteView):
	template_name = 'feed/post.html'
	model = Comment

	def get_object(self):
		obj = None
		if 'comment' in self.request.POST:
			pk = self.request.POST['comment']
			obj = Comment.objects.get(pk=pk, author=self.request.user)
		elif 'mypost' in self.request.POST:
			pk = self.request.POST['mypost']
			obj = myPost.objects.get(pk=pk, author=self.request.user)
		else:
			pass
		return obj

	def get_success_url(self):
		return self.request.META['HTTP_REFERER']


class EditPost(UpdateView):
	template_name = 'feed/post_form.html'
	model = myPost
	form_class = AddPostForm

	def dispatch(self, request, *args, **kwargs):
		self.object = get_object_or_404(myPost, author=request.user, pk=request.POST['mypost'])
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


class EditComment(PostDetail):

	def dispatch(self, request, *args, **kwargs):
		self.related_comment = get_object_or_404(Comment, pk=request.POST['comment'], author=request.user)
		pk = self.related_comment.post.id
		return super(EditComment, self).dispatch(request, pk=pk, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(EditComment, self).get_context_data(pk=self.related_comment.post.id, **kwargs)
		pk = self.related_comment.id
		context['editing'] = int(pk)
		context['form'] = AddCommentForm({'entry': self.related_comment.entry})
		return context

	def form_valid(self, form):
		setattr(self.related_comment, 'entry', form.cleaned_data['entry'])
		self.related_comment.save()
		return redirect(reverse('feed:post', kwargs={"pk": self.related_comment.post.id}))


class DeleteComment(DeleteView):
	template_name = 'feed/post.html'
	model = Comment

	def delete(self, request, *args, **kwargs):
		obj = self.get_object(queryset=None)
		if obj.author == self.request.user:
			super(DeleteComment, self).delete(request, *args, **kwargs)
			self.success_url = reverse('feed:detail', kwargs={"pk": object.post.pk})
		else:
			self.success_url = reverse('core:error', kwargs={'errors': 'Это не ваш комментарий!\t'})


class Rate(RedirectView, UpdateView):

	form_class = RateForm
	template_name = 'feed/rate_form.html'

	def form_valid(self, form):
		post = Post.objects.get(pk=form.cleaned_data["pk"])
		user = self.request.user

		RatedPost.objects.update_or_create(
			user=user,
			post=post,
			defaults={'mark': form.cleaned_data['mark']}
		)

		post.update_rating()

		if 'HTTP_REFERER' in self.request.META:
			return redirect(self.request.META['HTTP_REFERER'])
		else:
			return redirect(reverse('feed:detail', kwargs={'pk': post.id}))


def rate(request):
	if 'pk' in request.POST:
		post = get_object_or_404(myPost, pk=request.POST['pk'])
	else:
		return redirect(reverse('feed:feed'))

	if 'mark' in request.POST and abs(int(request.POST['mark'])) == 1:
		mark = int(request.POST['mark'])
	else:
		return redirect(reverse('core:error', kwargs={'errors': 'Не надо пытаться химичить с оценками!\t'}))

	user = request.user

	RatedPost.objects.update_or_create(
		user=user,
		post=post,
		defaults={'mark': mark}
	)

	post.update_rating()

	if 'HTTP_REFERER' in request.META:
		return redirect(request.META['HTTP_REFERER'])
	else:
		return redirect(reverse('feed:detail', kwargs={'pk': post.id}))


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


