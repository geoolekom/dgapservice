# coding: utf-8

from django.db import models
from core.models import User
from django.conf import settings
from redactor.fields import RedactorField
from django.utils.cache import caches
import logging

cache = caches['default']

logger = logging.getLogger(__name__)


class Post(models.Model):
	title = models.CharField(verbose_name='Заголовок', max_length=200)
	entry = RedactorField(
		verbose_name=u'Текст поста',
		redactor_options={'lang': 'кг', 'focus': True},
		upload_to='media/posts/',
		allow_file_upload=True,
		allow_image_upload=True,
	)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, parent_link=True)
	rating = models.IntegerField('Рейтинг', default=0)

	pub_time = models.DateTimeField('Время публикации', auto_now_add=True)
	upd_time = models.DateTimeField('Последнее изменение', auto_now=True)

	def __str__(self):
		return str(self.title)

	def summary(self):
		str_entry = str(self.entry)
		if len(str_entry) > 400:
			return str_entry[:400] + '...'
		else:
			return str_entry

	def in_details(self):
		return str(self.entry) + '\n(' + str(self.author) + ')'

	def change_rating(self, mark):
		self.rating += mark
		self.save()

	def update_rating(self):
		key = 'post_rating_' + str(self.id)
		self.rating = RatedPost.objects.filter(post=self).aggregate(rating_sum=models.Sum('mark'))['rating_sum']
		#for rated in RatedPost.objects.filter(post=self):
		#	self.rating += rated.mark
		cache.set(key, None)
		self.save()

	def get_rating(self):
		key = 'post_rating_' + str(self.id)
		cached_rating = cache.get(key)
		if cached_rating is None:
			cached_rating = self.rating
			cache.set(key, cached_rating, 5)
		else:
			print("FROM CACHE")
		return cached_rating

	def save(self, *args, **kwargs):
		super(Post, self).save(*args, **kwargs)
		cache.set('post_rating_' + str(self.id), None)
		logger.debug(str(self.author) + " saved post " + str(self.id))


class RatedPost(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	mark = models.IntegerField()


class Comment(models.Model):
	author = models.ForeignKey(settings.AUTH_USER_MODEL, parent_link=True)
	entry = RedactorField(
		verbose_name=u'Комментарий',
		redactor_options={'lang': 'ru', 'focus': True},
		upload_to='media/comments/',
		allow_file_upload=True,
		allow_image_upload=True,
	)
	post = models.ForeignKey(Post, parent_link=True)

	pub_time = models.DateTimeField('Время публикации', auto_now_add=True)
	upd_time = models.DateTimeField('Последнее изменение', auto_now=True)

	def __str__(self):
		return str(self.post) + ":\t" + str(self.entry)
	
	def save(self, *args, **kwargs):
		super(Comment, self).save(*args, **kwargs)
		logger.debug(str(self.author) + " saved comment " + str(self.id))
