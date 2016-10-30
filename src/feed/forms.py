from django import forms
from feed.models import Comment


class AddCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['entry']
