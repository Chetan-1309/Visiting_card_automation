"""
urls.py — URL routes for the cards app.
All under /cards/ (defined in main urls.py).

Full URLs:
  /cards/              → Card list (home)
  /cards/upload/       → Upload new card
  /cards/<id>/         → View card detail
  /cards/<id>/edit/    → Edit card data
  /cards/<id>/delete/  → Delete card
  /cards/export/       → Download Excel
  /cards/<id>/send/    → Send via Email/WhatsApp/SMS
"""

from django.urls import path
from . import views

urlpatterns = [
    path('',                  views.card_list,    name='card_list'),
    path('upload/',           views.card_upload,  name='card_upload'),
    path('<int:pk>/',         views.card_detail,  name='card_detail'),
    path('<int:pk>/edit/',    views.card_edit,    name='card_edit'),
    path('<int:pk>/delete/',  views.card_delete,  name='card_delete'),
    path('export/',           views.card_export,  name='card_export'),
    path('<int:pk>/send/',    views.card_send,    name='card_send'),
]
