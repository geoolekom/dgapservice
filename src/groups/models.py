from django.db import models
from library.models import Subject


class FacultyGroup(models.Model):
	group_number = models.CharField(primary_key=True, max_length=15)
	year = models.IntegerField()
	subjects = models.ManyToManyField(Subject, blank=True, verbose_name='Предметы')
	
	def __str__(self):
		return str(self.group_number)