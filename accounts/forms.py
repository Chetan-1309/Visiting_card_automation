"""
forms.py — Defines the HTML forms for Register and Login.
Django forms handle validation automatically (e.g. password match, email format).
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Form for new user registration.
    Extends Django's built-in UserCreationForm and adds email & phone.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'})
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '+91 9876543210'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose a username'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        # Store phone in the 'profile' field (or extend User model later)
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """
    Form for user login.
    Django's AuthenticationForm already handles username + password.
    We just customize the placeholders.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
