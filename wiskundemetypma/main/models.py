from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
# Create your models here.

class myUserCreationForm(forms.Form):
    username = forms.CharField(label='gebruikersnaam', min_length=4, max_length=64)
    id = forms.CharField(label='leerlingnummer', min_length=6, max_length=6) # MISSCHIEN DOEN WE DIT IDK MOET MET YPMA OVERLEGD WORDEN
    password1 = forms.CharField(label='wachtwoord', widget=forms.PasswordInput)
    password2 = forms.CharField(label='wachtwoord opnieuw', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("die gebruikersnaam bestaat al")
        return username

    def clean_leerlingnummer(self):
        id = self.cleaned_data['id']
        r = User.objects.filter(id=id)
        if r.count():
            raise ValidationError("dat leerlingnummer hebben wij al geregistreerd")
        return id
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('de wachtwoorden komen niet overeen')
        
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['id'],
            self.cleaned_data['password1']
        )
