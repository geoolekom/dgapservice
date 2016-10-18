from django.db import models

class Account(models.Model):
	balance = models.IntegerField(default=0)

	def refill(self, amount):
		# secure process of refilling
		balance += amount

	def withdraw(self, amount):
		# secure process of withdrowal
		balance -= amount
