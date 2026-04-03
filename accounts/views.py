"""
views.py — The "brain" of the accounts app.
A view is a Python function that:
  1. Receives an HTTP request (from the browser)
  2. Does some logic (check form, save data, etc.)
  3. Returns an HTTP response (an HTML page)
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def register_view(request):
    """
    Handles the Register page.
    GET  → Show the empty register form
    POST → Validate and save the new user
    """
    if request.user.is_authenticated:
        return redirect('card_list')  # Already logged in? Go to home.

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log them in after registering
            messages.success(request, f'Welcome, {user.username}! Account created.')
            return redirect('card_list')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()  # Empty form for GET request

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Handles the Login page.
    GET  → Show the empty login form
    POST → Check credentials and log in
    """
    if request.user.is_authenticated:
        return redirect('card_list')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('card_list')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Logs the user out and redirects to login page.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')
