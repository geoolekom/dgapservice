from django.db import models
from groups.models import FacultyGroup

class Shedule(models.Model):
	group = models.OneToOneField(FacultyGroup)
	day = models.DateField()
	lesson_number = models.IntegerField()
	lesson_title = models.CharField(max_length=50)
	teacher = models.CharField(max_length=50)
	room = models.IntegerField()

	def __str__(self):
		return str(self.group) + ':\t' + str(self.lesson_title)

