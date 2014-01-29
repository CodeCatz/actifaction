# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.utils.translation import ugettext as _
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, ButtonHolder, Layout


class UserAlreadyExistsError(Exception):
	pass


class LoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.form_tag = True
		self.helper.form_class = 'form-signin'
		self.helper.add_layout(Layout(
			Fieldset(_('Prijava'),
			         'username',
			         'password',
			),
			ButtonHolder(
				Submit('submit', _('Prijava'), css_class='btn btn-lg btn-primary btn-block'),
			),
		))


class UserCreateForm(UserCreationForm):
	email = forms.EmailField(
		label='Email naslov',
		required=True,
		error_messages={
			'required': 'Vnesite email naslov',
			'invalid': 'Email naslov ni pravilen'
		}
	)

	password1 = forms.CharField(label='Geslo', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Ponovi geslo', widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(UserCreateForm, self).__init__(*args, **kwargs)
		self.fields.pop('username')
		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.form_tag = True
		self.helper.form_class = 'form-signin'
		self.helper.add_layout(Layout(
			Fieldset(
				'Nov uporabnik',
				'email',
				'password1',
			    'password2',
			),
			ButtonHolder(
				Submit('submit', _('Registriraj'), css_class='btn btn-lg btn-primary btn-block'),
			),
		))

	def save(self, commit=True):
		user = super(UserCreateForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.username = self.cleaned_data['email']
		if commit:
			try:
				user.save()
			except IntegrityError:
				raise UserAlreadyExistsError
		return user


class UserProfileForm(forms.Form):
	first_name = forms.CharField(
		label='Ime',
	    required=False,
		max_length=255,
		error_messages={
			'invalid': 'Sorry, premalo prostora za tako dobro ime'
		}
	)

	last_name = forms.CharField(
		label='Priimek',
	    required=False,
		max_length=255,
		error_messages={
			'invalid': 'Sorry, premalo prostora za tako dobro ime'
		}
	)

	user_bio = forms.CharField(
		label='Bio',
		max_length=1024,
		required=False,
		widget=forms.Textarea,
	)

	avatar = forms.CharField(
		label='Slika uporabnika',
        required=False,
        widget=forms.FileInput(
            attrs={
                'title': 'Your ugly mug here'
            })
        )

	def __init__(self, *args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper()
		self.helper.form_method = 'POST'
		self.helper.form_tag = True
		self.helper.form_class = 'form-signin'
		self.helper.add_layout(Layout(
			Fieldset(_('Uporabniski profil'),
			         'first_name',
			         'last_name',
			         'user_bio',
			         'avatar',
			),
			ButtonHolder(
				Submit('submit', _('Dodaj'), css_class='btn btn-lg btn-primary btn-block'),
			),
		))