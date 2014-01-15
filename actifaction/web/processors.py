from django.contrib.auth.models import User
from api.models import UserProfile


def get_user(user_id):
	return User.objects.get(pk=user_id)


def get_user_profile(user_id):
	profile = UserProfile.objects.filter(user__pk=user_id)

	return profile


def get_user_profile(user_id):
	try:
		return UserProfile.objects.get(user__pk=user_id)
	except UserProfile.DoesNotExist:
		return None


def create_or_update_profile(user_id, **user_data):
	"""
    Creates or updates UserProfile object according to existance of user
    """
	user_profile = UserProfile.objects.filter(user__pk=user_id)

	if user_profile:
		user_profile = user_profile[0]
		user_profile.__dict__.update(user_data)
		user_profile.save()
	else:
		user_profile = UserProfile.objects.create(user=get_user(user_id), **user_data)

	return user_profile


