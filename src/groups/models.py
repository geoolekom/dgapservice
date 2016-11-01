from django.db import models


class FacultyGroup(models.Model):
	group_number = models.CharField(primary_key=True, max_length=15)
	year = models.IntegerField()
	
	def __str__(self):
		return self.group_number