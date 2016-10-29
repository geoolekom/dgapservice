from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views.generic.edit import FormView, CreateView
from core.forms import RegistrationForm
from core.models import User
from feed.models import Post


def login(request):
	username = request.POST['username']
	password = request.POST['password1']
	user = auth.authenticate(username=username, password=password)

	if user is not None and user.is_active:
		auth.login(request, user)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


class RegisterView(CreateView):
	template_name = "core/register.html"
	model = User
	form_class = RegistrationForm
	success_url = '/feed'

	def form_valid(self, form):
		ref = super(RegisterView, self).form_valid(form)
		user = form.save()
		if user is not None and user.is_active:
			auth.login(self.request, user)
		return ref

