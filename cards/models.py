"""
models.py — Defines the database tables using Python classes.
Each class = one table. Each attribute = one column.

Django will automatically create the actual SQL tables
when you run: python manage.py makemigrations && python manage.py migrate
"""

from django.db import models
from django.contrib.auth.models import User


class VisitingCard(models.Model):
    """
    Stores one uploaded visiting card and all its extracted data.

    Database columns:
      - owner        → which user uploaded this card (ForeignKey = link to User table)
      - photo        → the uploaded image file
      - name         → person's name (extracted by OCR)
      - job_title    → their job title
      - company      → company name
      - email        → email address
      - phone        → phone number
      - address      → office address
      - website      → website URL
      - raw_text     → full raw OCR text (useful for debugging)
      - created_at   → when it was uploaded
    """

    # ForeignKey means "each card belongs to one user"
    # on_delete=CASCADE means if user is deleted, their cards are deleted too
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cards'   # lets you do user.cards.all() later
    )

    # The actual image file — saved inside media/visiting_cards/
    photo = models.ImageField(upload_to='visiting_cards/')

    # Extracted fields — all optional (blank=True) because OCR might miss some
    name       = models.CharField(max_length=200, blank=True)
    job_title  = models.CharField(max_length=200, blank=True)
    company    = models.CharField(max_length=200, blank=True)
    email      = models.EmailField(blank=True)
    phone      = models.CharField(max_length=50, blank=True)
    address    = models.TextField(blank=True)
    website    = models.URLField(blank=True)

    # Full raw OCR output — useful to see everything the OCR found
    raw_text   = models.TextField(blank=True)

    # Auto-filled timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # set once on creation
    updated_at = models.DateTimeField(auto_now=True)       # updated every save

    class Meta:
        ordering = ['-created_at']  # newest cards first

    def __str__(self):
        # This controls how the card appears in Django Admin
        return f"{self.name or 'Unknown'} – {self.company or 'No Company'}"


class AdminSettings(models.Model):
    """
    A single settings row for the admin.
    Controls whether OCR processing is enabled.
    """
    processing_enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Admin Settings'
        verbose_name_plural = 'Admin Settings'

    def __str__(self):
        status = 'ON' if self.processing_enabled else 'OFF'
        return f'Card Processing: {status}'
