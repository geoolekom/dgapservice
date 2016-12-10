from django import forms
from feed.models import *
from redactor.widgets import RedactorEditor


class AddCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('entry', )


class AddPostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'entry', )

