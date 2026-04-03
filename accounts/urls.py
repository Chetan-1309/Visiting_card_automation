"""
urls.py — URL routes for the accounts app.
These are added under /accounts/ (see main urls.py).

So the full URLs are:
  /accounts/register/  → Register page
  /accounts/login/     → Login page
  /accounts/logout/    → Logout (redirects)
"""

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/',    views.login_view,    name='login'),
    path('logout/',   views.logout_view,   name='logout'),
]
