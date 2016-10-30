from django import forms
from groups.models import FacultyGroup as Group


class GroupChoiceForm(forms.Form):

	groups = Group.objects.all().order_by('group_number')
	group = forms.ChoiceField([(str(group), str(group)) for group in groups],
		label='',
		required=False)
