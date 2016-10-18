from django.db import models
from django.utils import timezone
from core.models import User
from django.conf import settings

class Post(models.Model):
	title = models.CharField('Title', max_length=200)
	entry = models.TextField('Content')
	author = models.ForeignKey(settings.AUTH_USER_MODEL, parent_link=True)
	rating = models.IntegerField('Rating', default=0)

	pub_time = models.DateTimeField('Pubication time', auto_now_add=True)
	upd_time = models.DateTimeField('Last update', auto_now=True)

	def __str__(self):
		return self.title

	def summary(self):
		strEntry = str(self.entry)
		if len(strEntry) > 350:
			return strEntry[:350] + '...'
		else:
			return strEntry

	def inDetails(self):
		return str(self.entry) + '\n(' + str(self.author) + ')'

	def changeRating(self, mark):
		self.rating += mark
		self.save()

	def likedBy(self):
	#	print("liked ", self, [a.user for a in RatedPost.objects.filter(post=self, mark=1)])
		return [a.user for a in RatedPost.objects.filter(post=self, mark=1)]

	def dislikedBy(self):
	#	print("disliked ", self, [a.user for a in RatedPost.objects.filter(post=self, mark=-1)])
		return [a.user for a in RatedPost.objects.filter(post=self, mark=-1)]

class RatedPost(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	mark = models.IntegerField()

