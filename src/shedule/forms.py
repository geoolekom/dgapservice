from django import forms
from shedule.models import Lesson


class EditLessonForm(forms.ModelForm):

	class Meta:
		model = Lesson
		fields = ('group', 'weekday', 'time_interval', 'subject', 'room', 'teacher', )

