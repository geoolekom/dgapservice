from django import forms
from feed.models import *


class AddCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('entry',)


class AddPostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'entry', )


class RateForm(forms.Form):

	choices = [post.pk for post in Post.objects.all()]

	pk = forms.ChoiceField(choices=choices)
	mark = forms.IntegerField()
