from django.contrib import auth
from django.views.generic.edit import FormView, CreateView
from django.views.generic import RedirectView
from core.forms import RegistrationForm, LoginForm
from core.models import User
from django.shortcuts import redirect, render
from django.core.urlresolvers import resolve


class LoginView(FormView):

	def dispatch(self, request, *args, **kwargs):
		self.form = LoginForm(request.POST)
		return super(LoginView, self).dispatch(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(LoginView, self).get_context_data(**kwargs)
		context['form'] = self.form
		return context

	def get_success_url(self):
		return self.request.META['HTTP_REFERER']

	def form_valid(self, form):
		auth.login(self.request, form.get_user())
		return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
	def get(self, request, *args, **kwargs):
		auth.logout(request)
		return super(LogoutView, self).get(request, *args, **kwargs)

	def get_redirect_url(self, *args, **kwargs):
		return self.request.META['HTTP_REFERER']


def login(request):
	username = request.POST['username']
	password = request.POST['password1']
	user = auth.authenticate(username=username, password=password)

	if user is not None and user.is_active:
		auth.login(request, user)
		return redirect(request.META['HTTP_REFERER'])
	else:
		return render(request, 'core/register.html', {'errors': 'Неправильное имя пользователя или пароль. Пройдите регистрацию.\t',
		                                              'form': RegistrationForm(request.POST)})


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

