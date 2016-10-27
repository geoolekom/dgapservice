from groups.models import FacultyGroup as Group
from shedule.models import Shedule
import datetime
from django.http import HttpResponse
from shedule.forms import GroupChoiceForm

from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
	
class SheduleListView(ListView):

    template_name = "shedule/shedule.html"
    day = datetime.date.today()

    def get_form(self):
    	try:
    		group = self.request.GET['group']
    		form = GroupChoiceForm(self.request.GET)
    	except:
    		try:
    			group = str(self.request.user.group)
    			form = GroupChoiceForm({'group': group})
    		except:
    			form = GroupChoiceForm()
    	return form

    def get_queryset(self):

    	form = self.get_form()

    	if form.is_valid():
    		group = Group.objects.get(group_number=form.cleaned_data['group'])
    		return Shedule.objects.filter(group=group)
    	else:
    		return Shedule.objects.none()

    def get_context_data(self, **kwargs):
    	parent = super(SheduleListView, self)
    	context = parent.get_context_data(**kwargs)
    	context['form'] = self.get_form()
    	context['days_of_week'] = range(1,8)

    	return context

