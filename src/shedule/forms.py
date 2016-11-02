from django import forms
from groups.models import FacultyGroup as Group
from shedule.models import Shedule


class GroupChoiceForm(forms.Form):

	groups = Group.objects.all().order_by('group_number')
	group = forms.ChoiceField([(str(group), str(group)) for group in groups],
		label='',
		required=False)


class EditSheduleForm(forms.ModelForm):

	class Meta:
		model = Shedule
		fields = ('group', 'day_of_week', 'lesson_number', 'lesson_title', 'teacher', 'room', )

