from django import forms
from library.models import Book


class ChooseBookForm(forms.ModelForm):
	class Meta:
		model = Book