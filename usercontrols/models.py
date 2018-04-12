from django.db import models
from django.urls import reverse

# Create your models here.
class User(models.Model):
	"""
	Model representing the user account
	"""
	username = models.CharField(primary_key=True, max_length=36)
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=36)
	
	"""
	#not working, cannot access .filter
	#def display_devices(self):
		
		Displays devices linked to user account
		
		#return ', '.join([Device.deviceid.filter(user__exact=self.username)])
	"""
	
	def get_absolute_url(self):
		"""
		URL to individual user details
		"""
		return reverse('user-detail', args=[str(self.id)])
		
	def __str__(self):
		"""
		String representing the User object
		"""
		return '{0}\n{1}'.format(self.username, self.email)

class Device(models.Model):
	"""
	Model for device information
	"""
	deviceid = models.CharField(primary_key=True, max_length=36)
	devicepsw = models.CharField(max_length=36)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	
	def __str__(self):
		"""
		String representing the User object
		"""
		return '{0}\n{1}'.format(self.deviceid, self.user.username)
