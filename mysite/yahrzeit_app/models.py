"""Models for yahrzeit app database."""

from django.db import models

# Create your models here.
class User(models.Model):
	"""Model for a User."""

	email= models.EmailField(max_length=100)
	password = models.CharField(max_length=30)

	def __repr__(self) -> str:
		"""String representation for User."""

		return f"<User username={self.username}>"

	def check_password(self, password: str) -> bool:
		"""Return True if password matches, False otherwise."""

		return password == self.password


class Decedent(models.Model):
	"""Model for a Decedent."""

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	death_date_hebrew = models.CharField(max_length=10)
	next_date_gregorian = models.DateField()
	
	def __repr__(self) -> str:
		"""String representation for Decedent."""

		return f"<Decedent name={self.name}>"
	