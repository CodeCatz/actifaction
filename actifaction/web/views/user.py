"""
User handling views
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response
from django.template import RequestContext
from api.models import UserProfile, Action

from web.forms.user_forms import UserCreateForm, UserProfileForm
from web.forms.user_forms import UserAlreadyExistsError

from web.processors.user import get_user, get_user_profile
from web.processors.user import create_or_update_profile


def register_user(request):
	form = UserCreateForm()

	if request.method == 'POST':
		form = UserCreateForm(request.POST)

	if form.is_valid():
		try:
			user = form.save()
			user = authenticate(username=request.POST['email'],
			                    password=request.POST['password1'])
			if user is not None:
				if user.is_active:
					create_or_update_profile(user.id)
					login(request, user)
					return HttpResponseRedirect(reverse('profile', args=[user.pk]))

		except UserAlreadyExistsError:
			messages.error(request, 'Uporabnik s tem emailom ze obstaja')

	return render_to_response(
		'user/registration.html', {
		'form': form,
		},
		context_instance=RequestContext(request))


@login_required
def profile(request, user_id):
	user = get_user(user_id)
	all_actions = Action.objects.filter(organizer=user)
	user_profile = get_user_profile(user_id)
	return render_to_response(
		'user/profile.html', {
		'user': user,
		'user_profile': user_profile,
		'actions': all_actions,
		},
		context_instance=RequestContext(request))


@login_required
def edit_profile(request, user_id):

	profile = get_user_profile(user_id)

	if profile:
		user_data = profile.__dict__
		user_data.update(profile.user.__dict__)
		form = UserProfileForm(initial=user_data)
	else:
		user = get_user(user_id)
		form = UserProfileForm(initial=user.__dict__)

	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES)
	if form.is_valid():

		user_data = {}
		user_data.update(form.cleaned_data)

		if request.FILES.get('avatar'):
			user_data['avatar'] = request.FILES['avatar']
		else:
			del user_data['avatar']

		create_or_update_profile(user_id, **user_data)
		return HttpResponseRedirect(reverse('profile', args=[user_id]))

	return render_to_response('user/profile_edit.html', {
		'form': form,
	    'profile': profile,
	}, context_instance=RequestContext(request))


