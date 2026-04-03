"""
admin.py — Registers our models with Django's built-in admin panel.
After this, you can manage cards and settings at http://127.0.0.1:8000/admin/
"""

from django.contrib import admin
from .models import VisitingCard, AdminSettings


@admin.register(VisitingCard)
class VisitingCardAdmin(admin.ModelAdmin):
    # Columns to show in the admin list view
    list_display  = ['name', 'company', 'email', 'phone', 'owner', 'created_at']
    # Sidebar filters
    list_filter   = ['created_at', 'owner']
    # Search bar
    search_fields = ['name', 'company', 'email']
    # Make date clickable for drill-down
    date_hierarchy = 'created_at'


@admin.register(AdminSettings)
class AdminSettingsAdmin(admin.ModelAdmin):
    list_display = ['processing_enabled', 'updated_at']
