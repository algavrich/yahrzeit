"""Models for yahrzeit app database."""

from django.db import models


class User(models.Model):
	"""Model for a User."""

	email= models.EmailField(max_length=100, unique=True)
	password = models.CharField(max_length=200)

	def __repr__(self) -> str:
		"""String representation for User."""

		return f"<User email={self.email}>"


class Decedent(models.Model):
	"""Model for a Decedent."""

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	death_date_hebrew = models.CharField(max_length=10)
	next_date_hebrew = models.CharField(max_length=10)
	next_date_gregorian = models.CharField(max_length=10)

	def __repr__(self) -> str:
		"""String representation for Decedent."""

		return f"<Decedent name={self.name}>"
