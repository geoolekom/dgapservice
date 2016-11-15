from groups.models import FacultyGroup as Group
from shedule.models import Lesson, Teacher, Auditory, rings, weekdays
from library.models import Subject
import datetime
from shedule.forms import EditLessonForm
from groups.forms import get_group_form

from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect, reverse


class LessonListView(ListView):
	template_name = 'shedule/shedule.html'
	today = datetime.date.today().weekday() + 1

	def dispatch(self, request, *args, **kwargs):
		group, self.group_form = get_group_form(request)
		self.edit_form = None

		if request.user.is_staff:
			if request.POST:
				self.edit_form = EditLessonForm({'group': group, 'time_interval': 0}, request.POST)
			else:
				self.edit_form = EditLessonForm({'group': group, 'time_interval': 0})

		return super(LessonListView, self).dispatch(request, args, kwargs)

	def get_queryset(self):
		if self.group_form.is_valid():
			group = Group.objects.get(group_number=self.group_form.cleaned_data['group'])
			return Lesson.objects.filter(group=group).order_by('time_interval')
		else:
			return Lesson.objects.none()

	def get_context_data(self, **kwargs):
		context = super(LessonListView, self).get_context_data(**kwargs)
		context['group_form'] = self.group_form
		context['weekdays'] = weekdays
		context['rings'] = rings
		context['today'] = self.today
		context['edit_form'] = self.edit_form
		return context


def edit_lesson(request):

	if request.POST and request.user.is_staff:

		group = get_object_or_404(Group, group_number=request.POST['group'])
		weekday = request.POST['weekday'] or 1
		time_interval = request.POST['time_interval'] or 0

		lesson, created = Lesson.objects.get_or_create(
			group=group,
			weekday=weekday,
			time_interval=time_interval
		)

		info = {
			'teacher': Teacher,
			'room': Auditory,
			'subject': Subject,
		}

		count = 0
		for name, clazz in info.items():
			try:
				pk = request.POST[name]
				obj = get_object_or_404(clazz, pk=pk)
				count += 1
				setattr(lesson, name, obj)
			except AttributeError:
				pass
			except ValueError:
				pass

		if lesson.subject is not None:
			group.subjects.add(lesson.subject)
			group.save()

		if count > 0:
			lesson.save()
		else:
			lesson.delete()

	if 'HTTP_REFERER' in request.META:
		return redirect(request.META['HTTP_REFERER'])
	return redirect(reverse('shedule:shedule'))

