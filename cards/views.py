"""
views.py — All the logic for the cards app.

Each function handles one URL/page:
  card_list    → /cards/           Show all cards with search/filter
  card_upload  → /cards/upload/    Upload a new card + run OCR
  card_detail  → /cards/<id>/      View a single card
  card_edit    → /cards/<id>/edit/ Edit extracted data
  card_delete  → /cards/<id>/del/  Delete a card
  card_export  → /cards/export/    Download all cards as Excel
  card_send    → /cards/<id>/send/ Send via Email/WhatsApp/SMS
"""

import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings

from .models import VisitingCard, AdminSettings
from .forms import CardUploadForm, CardEditForm, SendMessageForm, CardFilterForm
from .ocr import extract_text_from_image, parse_card_data


# ─── HELPER ────────────────────────────────────────────────────────────────────

def is_processing_enabled():
    """Check if admin has turned on card processing."""
    setting = AdminSettings.objects.first()
    if setting is None:
        return True  # Default: enabled
    return setting.processing_enabled


# ─── CARD LIST ─────────────────────────────────────────────────────────────────

@login_required  # ← User must be logged in to see this page
def card_list(request):
    """
    Shows all cards uploaded by the current user.
    Supports search and date filter.
    """
    # Get only THIS user's cards (not others')
    cards = VisitingCard.objects.filter(owner=request.user)

    form = CardFilterForm(request.GET)  # GET = search params in URL

    if form.is_valid():
        search = form.cleaned_data.get('search')
        from_date = form.cleaned_data.get('from_date')
        to_date = form.cleaned_data.get('to_date')

        if search:
            # Q objects let you do OR queries
            # This searches across name, company, and email
            cards = cards.filter(
                Q(name__icontains=search) |
                Q(company__icontains=search) |
                Q(email__icontains=search)
            )

        if from_date:
            cards = cards.filter(created_at__date__gte=from_date)

        if to_date:
            cards = cards.filter(created_at__date__lte=to_date)

    return render(request, 'cards/card_list.html', {
        'cards': cards,
        'form': form,
        'total': cards.count(),
    })


# ─── UPLOAD ────────────────────────────────────────────────────────────────────

@login_required
def card_upload(request):
    """
    Step 1: User uploads a visiting card photo.
    Django saves the image, runs OCR, extracts text, then redirects to edit page.
    """
    if not is_processing_enabled():
        messages.error(request, 'Card processing is currently disabled by the admin.')
        return redirect('card_list')

    if request.method == 'POST':
        form = CardUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the card (but don't commit to DB yet so we can add owner)
            card = form.save(commit=False)
            card.owner = request.user
            card.save()

            # Run OCR on the uploaded image
            image_path = card.photo.path  # Full path on disk
            raw_text = extract_text_from_image(image_path)
            extracted = parse_card_data(raw_text)

            # Save extracted data to the card
            card.raw_text  = extracted['raw_text']
            card.name      = extracted['name']
            card.job_title = extracted['job_title']
            card.company   = extracted['company']
            card.email     = extracted['email']
            card.phone     = extracted['phone']
            card.address   = extracted['address']
            card.website   = extracted['website']
            card.save()

            messages.success(request, 'Card uploaded! Please review the extracted data.')
            return redirect('card_edit', pk=card.pk)
    else:
        form = CardUploadForm()

    return render(request, 'cards/card_upload.html', {'form': form})


# ─── DETAIL ────────────────────────────────────────────────────────────────────

@login_required
def card_detail(request, pk):
    """View a single card. Only the owner can see their own card."""
    card = get_object_or_404(VisitingCard, pk=pk, owner=request.user)
    return render(request, 'cards/card_detail.html', {'card': card})


# ─── EDIT ──────────────────────────────────────────────────────────────────────

@login_required
def card_edit(request, pk):
    """
    Step 2: After OCR, user can correct any wrong fields.
    Pre-filled with OCR results.
    """
    card = get_object_or_404(VisitingCard, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = CardEditForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Card data saved successfully!')
            return redirect('card_detail', pk=card.pk)
    else:
        form = CardEditForm(instance=card)  # Pre-fill form with existing data

    return render(request, 'cards/card_edit.html', {'form': form, 'card': card})


# ─── DELETE ────────────────────────────────────────────────────────────────────

@login_required
def card_delete(request, pk):
    """Delete a card. Shows a confirmation page first."""
    card = get_object_or_404(VisitingCard, pk=pk, owner=request.user)

    if request.method == 'POST':
        # Also delete the actual image file from disk
        if card.photo and os.path.isfile(card.photo.path):
            os.remove(card.photo.path)
        card.delete()
        messages.success(request, 'Card deleted.')
        return redirect('card_list')

    return render(request, 'cards/card_confirm_delete.html', {'card': card})


# ─── EXCEL EXPORT ──────────────────────────────────────────────────────────────

@login_required
def card_export(request):
    """
    Exports all of the user's cards as an Excel (.xlsx) file.
    The browser will download the file automatically.
    """
    import openpyxl
    from openpyxl.styles import Font, PatternFill

    cards = VisitingCard.objects.filter(owner=request.user)

    # Create a new Excel workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Visiting Cards'

    # Header row with bold styling
    headers = ['#', 'Name', 'Job Title', 'Company', 'Email', 'Phone', 'Address', 'Website', 'Date']
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num, value=header)
        cell.font = Font(bold=True)
        cell.fill = PatternFill('solid', fgColor='4472C4')
        cell.font = Font(bold=True, color='FFFFFF')

    # Data rows
    for row_num, card in enumerate(cards, 2):
        ws.append([
            row_num - 1,
            card.name,
            card.job_title,
            card.company,
            card.email,
            card.phone,
            card.address,
            card.website,
            card.created_at.strftime('%Y-%m-%d'),
        ])

    # Auto-size columns
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 50)

    # Return as a downloadable response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="visiting_cards.xlsx"'
    wb.save(response)
    return response


# ─── SEND (Email / WhatsApp / SMS) ─────────────────────────────────────────────

@login_required
def card_send(request, pk):
    """Send card contact info via Email, WhatsApp, or SMS."""
    card = get_object_or_404(VisitingCard, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            channel   = form.cleaned_data['channel']
            recipient = form.cleaned_data['recipient']
            custom_msg = form.cleaned_data.get('message', '')

            # Build the default message text from card data
            card_text = (
                f"Contact Details:\n"
                f"Name: {card.name}\n"
                f"Title: {card.job_title}\n"
                f"Company: {card.company}\n"
                f"Email: {card.email}\n"
                f"Phone: {card.phone}\n"
                f"Website: {card.website}"
            )
            message_body = custom_msg if custom_msg else card_text

            try:
                if channel == 'email':
                    _send_email(recipient, card, message_body)
                elif channel == 'whatsapp':
                    _send_whatsapp(recipient, message_body)
                elif channel == 'sms':
                    _send_sms(recipient, message_body)

                messages.success(request, f'Successfully sent via {channel.title()}!')
                return redirect('card_detail', pk=card.pk)

            except Exception as e:
                messages.error(request, f'Failed to send: {str(e)}')
    else:
        # Pre-fill recipient with card's email if available
        form = SendMessageForm(initial={'recipient': card.email})

    return render(request, 'cards/card_send.html', {'form': form, 'card': card})


def _send_email(to_email, card, body):
    from django.core.mail import send_mail
    send_mail(
        subject=f'Contact: {card.name} – {card.company}',
        message=body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
    )


def _send_whatsapp(to_phone, body):
    from twilio.rest import Client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Ensure phone format
    if not to_phone.startswith("+"):
        to_phone = "+91" + to_phone

    client.messages.create(
        body=body,
        from_=f"whatsapp:{settings.TWILIO_WHATSAPP_NUMBER}",   # 🔥 Hardcode sandbox number
        to=f"whatsapp:{to_phone}"
    )


def _send_sms(to_phone, body):
    from twilio.rest import Client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to_phone
    )
