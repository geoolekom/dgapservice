from core.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm


class AdminUserAddForm(UserCreationForm):

	class Meta:
		model = User
		fields = ("username", "email", "password", "avatar")

	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User._default_manager.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(self.error_messages['Username is used.'])

	@staticmethod
	def clean_password():
		password = make_password("password")
		return password


class AdminUserChangeForm(UserChangeForm):

	class Meta:
		model = User
		fields = ("username", "email", "password", "avatar")


class RegistrationForm(UserCreationForm):

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "group", "email", "avatar")


class LoginForm(AuthenticationForm):
	pass
