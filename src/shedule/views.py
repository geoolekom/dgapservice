from django.shortcuts import render
from groups.models import FacultyGroup as Group
from shedule.models import Shedule
from django.utils import timezone
import datetime
from django.http import HttpResponse

def shedule(request, group_id):
	group = Group.objects.get(group_number=group_id)
	day = datetime.date.today()
	if request.user in group.user_set.all():
		context = {'object_list' : Shedule.objects.filter(group=group, day=day)}
		return render(request, 'shedule/shedule.html', context)
	else:
		return HttpResponse("Not yours group.")

	



