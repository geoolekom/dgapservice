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


class CustomizeFeedForm(forms.Form):
	searchstr = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Поиск'}), required=False)
	sort_by = forms.ChoiceField(choices=[("-pub_time", "Новые сверху"), ("-rating", "Лучшие сверху")], label='')
