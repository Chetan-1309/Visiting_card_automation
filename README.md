# 📇 Visiting Card Automation System
### Built with Django + Plain HTML/CSS

---

## 🗂 Project Structure

```
visitingcard/              ← Root folder
│
├── manage.py              ← Run commands here
├── requirements.txt       ← List of packages to install
├── .env                   ← Your secret keys (DON'T share this!)
├── .gitignore             ← Files to exclude from git
│
├── visitingcard/          ← Main project config
│   ├── settings.py        ← All Django settings
│   ├── urls.py            ← Main URL router
│   └── wsgi.py            ← Server entry point
│
├── accounts/              ← Register / Login app
│   ├── forms.py           ← Register & Login forms
│   ├── views.py           ← Logic for register/login/logout
│   └── urls.py            ← /accounts/... routes
│
├── cards/                 ← Visiting Card app
│   ├── models.py          ← Database tables (VisitingCard, AdminSettings)
│   ├── forms.py           ← Upload, Edit, Send, Filter forms
│   ├── views.py           ← All card logic
│   ├── urls.py            ← /cards/... routes
│   ├── admin.py           ← Django admin registration
│   └── ocr.py             ← OCR text extraction logic
│
├── templates/             ← All HTML files
│   ├── base.html          ← Shared navbar/layout
│   ├── accounts/
│   │   ├── register.html
│   │   └── login.html
│   └── cards/
│       ├── card_list.html
│       ├── card_upload.html
│       ├── card_edit.html
│       ├── card_detail.html
│       ├── card_confirm_delete.html
│       └── card_send.html
│
├── static/css/style.css   ← Main stylesheet
└── media/                 ← Uploaded card photos (auto-created)
```

---

## 🚀 Step-by-Step Setup

### Step 1 — Open Terminal / Command Prompt
Navigate to the folder where you want your project:
```
cd Desktop
```

### Step 2 — Create a Virtual Environment
A virtual environment keeps this project's packages separate from other projects.
```bash
python -m venv venv
```

Activate it:
- **Windows:**  `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

You'll see `(venv)` appear in your terminal. That means it's working!

### Step 3 — Copy the Project Files
Copy the `visitingcard/` folder (these files) into your current directory.

### Step 4 — Install All Packages
```bash
pip install -r requirements.txt
```
This installs Django, Pillow (images), pytesseract (OCR), openpyxl (Excel), Twilio (SMS/WhatsApp).

### Step 5 — Install Tesseract OCR Engine
Pytesseract needs the actual Tesseract program installed on your computer.

- **Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki
  After installing, add this to `cards/ocr.py` at the top:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```
- **Mac:**     `brew install tesseract`
- **Ubuntu:**  `sudo apt install tesseract-ocr`

### Step 6 — Configure Your .env File
Open `.env` and fill in your details:
```
SECRET_KEY=any-random-long-string-here
DEBUG=True
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
```
For Gmail app password: Google Account → Security → 2-Step → App Passwords

### Step 7 — Set Up the Database
```bash
python manage.py makemigrations
python manage.py migrate
```
This creates the database file (`db.sqlite3`) and all tables.

### Step 8 — Create an Admin Account
```bash
python manage.py createsuperuser
```
Enter a username, email, and password. This is for the /admin/ panel.

### Step 9 — Run the Server
```bash
python manage.py runserver
```
Open your browser and go to: **http://127.0.0.1:8000**

---

## 🌐 Available Pages

| URL | Page |
|-----|------|
| http://127.0.0.1:8000/accounts/register/ | Register |
| http://127.0.0.1:8000/accounts/login/ | Login |
| http://127.0.0.1:8000/cards/ | My Cards (Home) |
| http://127.0.0.1:8000/cards/upload/ | Upload Card |
| http://127.0.0.1:8000/cards/export/ | Download Excel |
| http://127.0.0.1:8000/admin/ | Admin Panel |

---

## ❓ Common Errors & Fixes

**"ModuleNotFoundError: No module named 'django'"**
→ Make sure your virtual environment is activated: `venv\Scripts\activate`

**"tesseract is not installed or not in PATH"**
→ Install Tesseract (Step 5) and set the path in ocr.py

**"No such table: cards_visitingcard"**
→ Run: `python manage.py migrate`

**Image not showing after upload**
→ Check that `MEDIA_URL` and `MEDIA_ROOT` are set in settings.py (already done)

---

## 📦 What Each Package Does

| Package | Purpose |
|---------|---------|
| Django | The web framework — handles URLs, views, database, forms |
| Pillow | Lets Django work with image files |
| pytesseract | Python wrapper for Tesseract OCR |
| openpyxl | Creates .xlsx Excel files |
| python-decouple | Reads secrets from .env file |
| twilio | Sends SMS and WhatsApp messages |
