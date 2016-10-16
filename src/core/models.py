from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

	avatar = models.ImageField('Avatar', upload_to='avatars/', blank=True)
	group_number = models.CharField('Group', max_length=10, blank=True)

	rated_posts = []

	def __str__(self):
		return self.username