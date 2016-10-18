from django.db import models
from django.contrib.auth.models import AbstractUser
from groups.models import FacultyGroup
from money.models import Account

class User(AbstractUser):

	avatar = models.ImageField('Avatar', upload_to='avatars/', blank=True, null=True)
	group = models.ForeignKey(FacultyGroup, blank=True, null=True)
	account = models.OneToOneField(Account, blank=True, null=True)
	room = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.username