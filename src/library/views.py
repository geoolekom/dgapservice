from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from groups.forms import get_group_form
from library.models import Subject
from groups.models import FacultyGroup as Group


class BookListView(ListView):
	template_name = 'library/subject_list.html'
	model = Subject

	def dispatch(self, request, *args, acts=None, **kwargs):
		group_number, self.group_form = get_group_form(request)
		try:
			self.active_subject = Subject.objects.get(pk=acts)
		except Subject.DoesNotExist:
			self.active_subject = None
		return super(BookListView, self).dispatch(request, *args, **kwargs)

	def get_queryset(self):
		if self.group_form.is_valid():
			group = Group.objects.get(group_number=self.group_form.cleaned_data['group'])
			return group.subjects.all()
		else:
			return Subject.objects.none()

	def get_context_data(self, **kwargs):
		context = super(BookListView, self).get_context_data(**kwargs)
		context['group_form'] = self.group_form
		context['active_subject'] = self.active_subject
		return context
