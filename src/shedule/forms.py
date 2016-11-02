from django import forms
from shedule.models import Shedule


class EditSheduleForm(forms.ModelForm):

	class Meta:
		model = Shedule
		fields = ('group', 'day_of_week', 'lesson_number', 'lesson_title', 'teacher', 'room', )

