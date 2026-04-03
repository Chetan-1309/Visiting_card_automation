"""
forms.py — Forms for the cards app.

CardUploadForm  → Just the photo upload field
CardEditForm    → Edit all extracted fields after OCR
SendMessageForm → Choose channel (Email/WhatsApp/SMS) and message
"""

from django import forms
from .models import VisitingCard


class CardUploadForm(forms.ModelForm):
    """Simple form — just choose a photo to upload."""
    class Meta:
        model = VisitingCard
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'accept': 'image/*'})
        }


class CardEditForm(forms.ModelForm):
    """
    After OCR runs, the user can review and correct the extracted data.
    All fields are editable.
    """
    class Meta:
        model = VisitingCard
        fields = ['name', 'job_title', 'company', 'email', 'phone', 'address', 'website']
        widgets = {
            'name':      forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'job_title': forms.TextInput(attrs={'placeholder': 'Job Title'}),
            'company':   forms.TextInput(attrs={'placeholder': 'Company Name'}),
            'email':     forms.EmailInput(attrs={'placeholder': 'email@company.com'}),
            'phone':     forms.TextInput(attrs={'placeholder': '+91 9876543210'}),
            'address':   forms.Textarea(attrs={'rows': 3, 'placeholder': 'Office Address'}),
            'website':   forms.URLInput(attrs={'placeholder': 'https://www.example.com'}),
        }


class SendMessageForm(forms.Form):
    """Form to send a card's contact info via Email, WhatsApp, or SMS."""
    CHANNEL_CHOICES = [
        ('email',     '📧 Email'),
        ('whatsapp',  '💬 WhatsApp'),
        ('sms',       '📱 SMS'),
    ]
    channel    = forms.ChoiceField(choices=CHANNEL_CHOICES, widget=forms.RadioSelect)
    recipient  = forms.CharField(max_length=200, help_text='Email address or phone number')
    message    = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False,
                                  help_text='Optional custom message')


class CardFilterForm(forms.Form):
    """Search and filter form for the card list page."""
    search  = forms.CharField(required=False, widget=forms.TextInput(
                  attrs={'placeholder': 'Search name, company, email...'}))
    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    to_date   = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
