# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


class SignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        help_text='Enter your date of birth.',
    )
    class Meta:
        model = CustomUser
        fields = ['firstname', 'surname','username', 'email', 'password1', 'password2', 'position', 'date_of_birth', 'location', 'department', 'phone']

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class LeaveForm(forms.ModelForm):
    end_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        help_text='Enter your end date.',
    )
    start_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}),
        help_text='Enter your start date.',
    )
    class Meta:
        model = LeaveRequest
        fields = ['leave_type','start_date','end_date','reason','relieving_Officer']
