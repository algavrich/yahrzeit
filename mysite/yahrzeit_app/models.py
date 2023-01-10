from django.db import models

# Create your models here.
class User(models.Model):
	username= models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	email= models.CharField(max_length=30)

	def __repr__(self):
		return f"<User username={self.username}>"

class Decedent(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)
	death_date_hebrew = models.CharField(max_length=10)
	next_date_gregorian = models.DateField()
	
	def __repr__(self):
		return f"<Decedent name={self.name}>"
	