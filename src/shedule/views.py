from groups.models import FacultyGroup as Group
from shedule.models import Shedule
import datetime
from shedule.forms import GroupChoiceForm

from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404


class SheduleListView(ListView):
	template_name = 'shedule/shedule.html'
	today = datetime.date.today().weekday() + 1

	def dispatch(self, request, *args, **kwargs):
		try:
			self.request.GET['group']
			self.form = GroupChoiceForm(self.request.GET)
		except KeyError:
			try:
				group = str(self.request.user.group)
				self.form = GroupChoiceForm({'group': group})
			except:
				self.form = GroupChoiceForm()
		return super(SheduleListView, self).dispatch(request, args, kwargs)

	def get_queryset(self):

		form = self.form
		if form.is_valid():
			group = Group.objects.get(group_number=form.cleaned_data['group'])
			return Shedule.objects.filter(group=group)
		else:
			return Shedule.objects.none()

	def get_context_data(self, **kwargs):
		parent = super(SheduleListView, self)
		context = parent.get_context_data(**kwargs)
		context['shedule_form'] = self.form
		context['days_of_week'] = range(1, 7)
		context['today'] = self.today
		return context

