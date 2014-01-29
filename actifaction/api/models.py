from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class ActionCategory(models.Model):
	name = models.CharField(max_length=255) #we don't want to limit ourselves here, we'll rather do this in GUI
	slug = models.CharField(max_length=255)
	description = models.TextField(max_length=255,blank=True)

	def __unicode__(self):
		return '%s' % self.name

	class Meta:
		verbose_name_plural = "Action categories"


class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	user_bio = models.TextField(max_length=1024)
	avatar = models.ImageField(upload_to='user_avatars', default='http://placehold.it/30x30')

	def __unicode__(self):
		return '%s' % self.user.email


class Action(models.Model):
	creation_date = models.DateField(auto_now_add = True)
	title = models.CharField(max_length=50)
	location = models.CharField(max_length=50)
	description = models.TextField(max_length=255)
	action_date = models.DateTimeField()
	action_type = models.ForeignKey(ActionCategory)
	max_people = models.IntegerField(null=True,blank=True)
	organizer = models.ForeignKey(User)
	attendees = models.ManyToManyField(User, related_name="attendee_of")

	
	def get_attendees_profiles(self):
		profiles = []
		list_of_attendees = self.attendees.all()
		for user in list_of_attendees:
			profile = UserProfile.objects.get(user__pk=user.id)
			profiles.append(profile)
		return profiles
	profiles=property(get_attendees_profiles)

	def __unicode__(self):
		return '%s' % self.title

