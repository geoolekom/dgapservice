from django import forms
from groups.models import FacultyGroup as Group
from django.utils.functional import lazy
from random import choice


class GroupChoiceForm(forms.Form):

#	year = forms.ChoiceField([(i, str(i) + " курс") for i in range(1, 7)], label='', required=False)
	groups = Group.objects.all().order_by('group_number')

	choices = [(str(group), group.pk) for group in groups]
	group = forms.ChoiceField(choices=choices, label='', required=False)


def get_group_form(request):
	if 'group' in request.GET:
		group = request.GET['group']
		group_form = GroupChoiceForm(request.GET)
	else:
		try:
			group = request.user.group_id
		#	year = str(request.user.group.year)
			group_form = GroupChoiceForm({'group': request.user.group_id})
		except:
			group = None
			group_form = GroupChoiceForm()

	return group, group_form

