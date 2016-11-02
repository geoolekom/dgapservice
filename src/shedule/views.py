from groups.models import FacultyGroup as Group
from shedule.models import Shedule
import datetime
from shedule.forms import GroupChoiceForm, EditSheduleForm

from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404, redirect, reverse


class SheduleListView(ListView):
	template_name = 'shedule/shedule.html'
	today = datetime.date.today().weekday() + 1

	def dispatch(self, request, *args, **kwargs):
		self.edit_form = None
		if 'group' in request.GET:
			group = request.GET['group']
			self.group_form = GroupChoiceForm(self.request.GET)
		else:
			try:
				group = str(self.request.user.group)
				self.group_form = GroupChoiceForm({'group': group})
			except:
				self.group_form = GroupChoiceForm()

		if request.user.is_staff:
			if request.POST:
				self.edit_form = EditSheduleForm({'group': group}, request.POST)
			else:
				self.edit_form = EditSheduleForm({'group': group})

		return super(SheduleListView, self).dispatch(request, args, kwargs)

	def get_queryset(self):

		if self.group_form.is_valid():
			group = Group.objects.get(group_number=self.group_form.cleaned_data['group'])
			return Shedule.objects.filter(group=group)
		else:
			return Shedule.objects.none()

	def get_context_data(self, **kwargs):
		parent = super(SheduleListView, self)
		context = parent.get_context_data(**kwargs)
		context['group_form'] = self.group_form
		context['days_of_week'] = {1: 'Понедельник', 2: 'Вторник', 3: 'Среда', 4: 'Четверг', 5: 'Пятница', 6: 'Суббота'}
		context['today'] = self.today
		context['edit_form'] = self.edit_form
		return context


def edit_shedule(request):
	if request.POST:

		group = get_object_or_404(Group, group_number=request.POST['group'])
		day_of_week = request.POST['day_of_week']
		lesson_number = request.POST['lesson_number']

		shedule, created = Shedule.objects.get_or_create(group=group, day_of_week=day_of_week, lesson_number=lesson_number)

		lesson_title = request.POST['lesson_title'] or shedule.lesson_title
		teacher = request.POST['teacher'] or shedule.teacher
		room = request.POST['room'] or shedule.room
		setattr(shedule, 'lesson_title', lesson_title)
		setattr(shedule, 'teacher', teacher)
		setattr(shedule, 'room', room)
		shedule.save()

	if 'HTTP_REFERER' in request.META:
		return redirect(request.META['HTTP_REFERER'])
	return redirect(reverse('feed:feed'))

