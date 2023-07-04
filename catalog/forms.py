from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms import ModelForm
from .models import Stih, Author
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import datetime 

class StihForm(forms.Form):
    stih_checked = forms.BooleanField(required=False)

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	birth_date = forms.DateField(required=True)

	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "birth_date", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.birth_date = self.cleaned_data['birth_date']
		if commit:
			user.save()
		return user