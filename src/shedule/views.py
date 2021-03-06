from groups.models import FacultyGroup as Group
from shedule.models import Lesson, Teacher, Auditory, rings, weekdays
from library.models import Subject
import datetime
from shedule.forms import EditLessonForm
from groups.forms import get_group_form

from django.views.generic import ListView, UpdateView, DetailView
from django.shortcuts import get_object_or_404, redirect, reverse
from django.http import JsonResponse
from django.db.models import F, Q


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
			group = Group.objects.get(pk=self.group_form.cleaned_data['group'])
			self.queryset = Lesson.objects\
				.filter(group=group)\
				.select_related('room')\
				.select_related('subject')\
				.select_related('teacher')\
				.order_by('time_interval')
			if 'recently_changed' in self.request.GET and self.request.GET['recently_changed'] == 'true':
				self.queryset = self.queryset.filter(Q(upd_time__gt=F('pub_time')) & Q(upd_time__gt=datetime.datetime.now() - datetime.timedelta(days=1)))
		else:
			self.queryset = Lesson.objects.none()

		return self.queryset

	def get_context_data(self, **kwargs):
		context = super(LessonListView, self).get_context_data(**kwargs)
		context['group_form'] = self.group_form
		context['weekdays'] = weekdays
		context['rings'] = rings
		context['today'] = self.today
		context['edit_form'] = self.edit_form
		return context


class LessonUpdateView(UpdateView):
	model = Lesson
	form_class = EditLessonForm
	template_name = 'shedule/edit_lesson_form.html'
	success_url = '/shedule'


class LessonDetailView(DetailView):
	model = Lesson

	def get(self, request, *args, **kwargs):
		lesson = self.get_object()
		data = {
			'time_interval': lesson.time_interval,
			'room': lesson.room,
			'subject': lesson.subject,
			'teacher': lesson.teacher,
		}
		return JsonResponse(data)


