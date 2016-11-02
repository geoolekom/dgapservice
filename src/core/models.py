from django.db import models
from django.contrib.auth.models import AbstractUser
from groups.models import FacultyGroup
from django.shortcuts import reverse


class User(AbstractUser):

	def user_avatars_path(self, filename):
		return 'avatars/{0}'.format(self.username)

	avatar = models.ImageField('Avatar', upload_to=user_avatars_path, blank=True, null=True)
	group = models.ForeignKey(FacultyGroup, blank=True, null=True)
	room = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return str(self.username)
