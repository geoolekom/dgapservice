# coding: utf-8

from django.db import models
from core.models import User
from django.conf import settings


class Post(models.Model):
	title = models.CharField(verbose_name='Заголовок', max_length=200)
	entry = models.TextField(verbose_name="Текст поста")
	author = models.ForeignKey(settings.AUTH_USER_MODEL, parent_link=True)
	rating = models.IntegerField('Рейтинг', default=0)

	pub_time = models.DateTimeField('Время публикации', auto_now_add=True)
	upd_time = models.DateTimeField('Последнее изменение', auto_now=True)

	def __str__(self):
		return str(self.title)

	def summary(self):
		strEntry = str(self.entry)
		if len(strEntry) > 400:
			return strEntry[:400] + '...'
		else:
			return strEntry

	def in_details(self):
		return str(self.entry) + '\n(' + str(self.author) + ')'

	def changeRating(self, mark):
		self.rating += mark
		self.save()

	def likedBy(self):
		return [a.user for a in RatedPost.objects.filter(post=self, mark=1)]

	def dislikedBy(self):
		return [a.user for a in RatedPost.objects.filter(post=self, mark=-1)]


class RatedPost(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	mark = models.IntegerField()


class Comment(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, parent_link=True)
	entry = models.TextField(verbose_name='Комментарий')
	post = models.ForeignKey(Post, parent_link=True)

	pub_time = models.DateTimeField('Время публикации', auto_now_add=True)
	upd_time = models.DateTimeField('Последнее изменение', auto_now=True)

	def __str__(self):
		return str(self.post) + ":\t" + str(self.entry)
