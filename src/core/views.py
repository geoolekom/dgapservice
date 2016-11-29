from django.contrib import auth
from django.views.generic.edit import FormView, CreateView
from core.forms import RegistrationForm, LogoutForm
from core.models import User
from django.shortcuts import redirect, render
from django.shortcuts import reverse
from django.contrib.auth.forms import AuthenticationForm


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

