from django.db import models
from django.conf import settings


class Account(models.Model):
	balance = models.IntegerField(default=0)
	user = models.OneToOneField(settings.AUTH_USER_MODEL)

	def __str__(self):
		return str(self.user) + ": " + str(self.balance)


class Operation(models.Model):
	account = models.ForeignKey(Account)
	sum = models.IntegerField()
	comment = models.CharField(max_length=100)

	def provide(self):
		self.account.balance += sum
		pass

