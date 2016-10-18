from django.db import models
from core.models import User
from django.conf import settings

class Service(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, parent_link=True, default=1)
	date = models.DateTimeField(auto_now=True)

class Print(models.Model):
	service = models.OneToOneField(Service, parent_link=True)

	def document_path(instance, filename):
		return 'documents/{0}/{1}'.format(instance.service.user.username, filename)

	document = models.FileField(upload_to=document_path)
	printer = models.IntegerField(blank=True, null=True)

class FoodDelievery(models.Model):
	service = models.OneToOneField(Service, parent_link=True)

	room = models.IntegerField(blank=True, null=True)
	dish = models.URLField(blank=True, null=True)

class Laundry(models.Model):
	service = models.OneToOneField(Service, parent_link=True)

	beg_time = models.DateTimeField(blank=True, null=True)
	end_time = models.DateTimeField(blank=True, null=True)
