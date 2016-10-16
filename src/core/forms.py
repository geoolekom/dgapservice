from core.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.hashers import make_password

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

	def clean_password(self):
		password = make_password("password")
		return password

class AdminUserChangeForm(UserChangeForm):

	class Meta:
		model = User
		fields = ("username", "email", "password", "avatar")