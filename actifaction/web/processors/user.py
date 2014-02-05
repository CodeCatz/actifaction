from django.contrib.auth.models import User
from api.models import UserProfile


def get_user(user_id):
	try:
		return User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return None


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
	if not user_data:
		user=get_user(user_id)
		user_profile=UserProfile.objects.create(user=user)
		return user_profile

	user_profile = UserProfile.objects.filter(user__pk=user_id)
	if user_profile:
		user_profile = user_profile[0]
		user_profile.__dict__.update(user_data)
		user_profile.user.__dict__.update(user_data)
		user_profile.user.save()
		user_profile.save()
	else:
		current_user = get_user(user_id)
		current_user.firstname=user_data['first_name']
		current_user.lastname=user_data['last_name']
		current_user.save()
		user_profile = UserProfile.objects.create(user=get_user(user_id),
		                                          user_bio=user_data['user_bio'],
		                                          avatar=user_data['avatar']
		                                          )


	return user_profile


