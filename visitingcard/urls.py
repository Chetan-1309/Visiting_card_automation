"""
urls.py — The "traffic director" of your project.
When someone visits a URL, Django looks here to decide which app handles it.

URL Structure:
  /               → Redirects to /cards/ (home)
  /accounts/...   → Register, Login, Logout
  /cards/...      → Upload, List, Export, Send
  /admin/         → Django built-in admin panel
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    # Root URL → redirect to cards home
    path('', lambda request: redirect('card_list'), name='home'),

    # Django built-in admin panel (e.g. /admin/)
    path('admin/', admin.site.urls),

    # Our accounts app (register, login, logout)
    path('accounts/', include('accounts.urls')),

    # Our cards app (upload, list, export, send)
    path('cards/', include('cards.urls')),
]

# This tells Django to serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
