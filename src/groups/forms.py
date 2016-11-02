from django import forms
from groups.models import FacultyGroup as Group


class GroupChoiceForm(forms.Form):

	groups = Group.objects.all().order_by('group_number')
	group = forms.ChoiceField([(str(group), str(group)) for group in groups],
		label='',
		required=False)


def get_group_form(request):
	if 'group' in request.GET:
		group = request.GET['group']
		group_form = GroupChoiceForm(request.GET)
	else:
		try:
			group = str(request.user.group)
			group_form = GroupChoiceForm({'group': group})
		except:
			group = None
			group_form = GroupChoiceForm()

	return group, group_form

