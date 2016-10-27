from django.db import models

class FacultyGroup(models.Model):
	group_number = models.IntegerField(primary_key=True)
	year = models.IntegerField()
	
	def __str__(self):
		return str(self.group_number)