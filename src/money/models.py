from django.db import models
from core.models import User
from django.conf import settings

class Account(models.Model):
	balance = models.IntegerField(default=0)
	user = models.OneToOneField(settings.AUTH_USER_MODEL)

	def refill(self, amount):
		# secure process of refilling
		balance += amount

	def withdraw(self, amount):
		# secure process of withdrowal
		balance -= amount

	def __str__(self):
		return str(self.user) + ": " + str(self.balance)
