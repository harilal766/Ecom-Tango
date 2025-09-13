from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class BaseAuthForm(AuthenticationForm):
    attributes = {"class" : "form"}
    username = forms.CharField(widget=TextInput(attrs = {"class" : "form", "placehoder" : "Username"}))
    password = forms.CharField(widget=TextInput(attrs = {"class" : "form", "placehoder" : "Username"}))

class LoginForm(BaseAuthForm):
    pass

