from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
# Create your models here.

class myUserCreationForm(forms.Form):
    username = forms.CharField(label='Gebruikersnaam', min_length=4, max_length=64)
    pk = forms.CharField(label='Leerlingnummer', min_length=6, max_length=6) # MISSCHIEN DOEN WE DIT IDK MOET MET YPMA OVERLEGD WORDEN
    email = forms.EmailField(label='Emailadres')
    password1 = forms.CharField(label='Wachtwoord', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Wachtwoord opnieuw', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("die gebruikersnaam bestaat al")
        return username

    def clean_leerlingnummer(self):
        pk = self.cleaned_data['pk']
        return pk


    def clean_email(self):
        email = self.cleaned_data['email']
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError("die email hebben wij al geregistreerd ")
        return email

    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('de wachtwoorden komen niet overeen')
        
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['pk'],
            self.cleaned_data['password1']
        )
