from django.contrib import auth
from django.views.generic.edit import FormView, CreateView
from core.forms import RegistrationForm, LoginForm
from core.models import User
from django.shortcuts import redirect, render
from django.shortcuts import reverse


def logout(request):
	auth.logout(request)
	return redirect(reverse('feed:feed'))


def login(request):
	if 'HTTP_REFERER' in request.META:
		redirect_url = request.META['HTTP_REFERER']
		if 'username' in request.POST and 'password1' in request.POST:
			username = request.POST['username']
			password = request.POST['password1']
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				auth.login(request, user)
				return redirect(redirect_url)
			else:
				return render(request, 'core/base.html',
				              {'errors': 'Неправильное имя пользователя или пароль.\t'})
		else:
			return render(request, 'core/base.html',
			       {'errors': 'Вы не ввели имя пользователя или пароль.\t'})
	else:
		return render(request, 'core/base.html',
		       {'errors': 'Вы пришли непонятно откуда и не ввели имя пользователя и пароль.\t'})


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

