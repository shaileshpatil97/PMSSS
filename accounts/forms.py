from django import forms
from .models import User, StudentProfile

class StudentRegistrationForm(forms.Form):
    aadhaar = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput)
    full_name = forms.CharField(max_length=100)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    mobile = forms.CharField(max_length=10)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)

class LoginForm(forms.Form):
    aadhaar = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput)

