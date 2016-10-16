from django.db import models
from django.utils import timezone
from core.models import User
from django.conf import settings

class Post(models.Model):
	title = models.CharField('Title', max_length=200)
	entry = models.TextField('Content')
	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	rating = models.IntegerField('Rating', default=0)

	pub_time = models.DateTimeField('Pubication time', auto_now_add=True)
	upd_time = models.DateTimeField('Last update', auto_now_add=True)

	def __str__(self):
		return self.title

	def summary(self):
		strEntry = str(self.entry)
		if len(strEntry) > 120:
			return strEntry[:120] + '...'
		else:
			return strEntry

	def inDetails(self):
		return str(self.entry) + '\n(' + str(self.author) + ')'

