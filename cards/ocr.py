"""
ocr.py — Final version with aggressive name detection + debug output.
"""

import re
import pytesseract
from PIL import Image, ImageOps, ImageEnhance

# ── WINDOWS: Tesseract path ──
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def preprocess_image(img):
    gray = img.convert('L')
    inverted = ImageOps.invert(gray)
    inv_contrast = ImageEnhance.Contrast(inverted).enhance(3.0)
    inv_bright = ImageEnhance.Brightness(inverted).enhance(1.5)
    high_contrast = ImageEnhance.Contrast(gray).enhance(3.0)

    best_text = ''
    for v in [inv_contrast, inv_bright, inverted, gray, high_contrast]:
        w, h = v.size
        # Try even bigger scale for bold text
        for scale in [3, 2]:
            v_large = v.resize((w * scale, h * scale), Image.LANCZOS)
            for psm in ['6', '4', '3']:
                text = pytesseract.image_to_string(
                    v_large,
                    config=f'--psm {psm} --oem 3'
                )
                if len(text.strip()) > len(best_text.strip()):
                    best_text = text
    return best_text


def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path).convert('RGB')
        return preprocess_image(img).strip()
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""


def clean_line(line):
    """Remove non-printable/non-ASCII characters from a line."""
    return re.sub(r'[^\x20-\x7E]', '', line).strip()


def parse_card_data(raw_text):
    # Clean each line of garbage characters
    lines = [clean_line(line) for line in raw_text.split('\n')]
    lines = [l for l in lines if l]  # remove empty

    # ── DEBUG: print every line to terminal ──────────────────────────────
    print("\n========== OCR DEBUG ==========")
    for i, line in enumerate(lines):
        print(f"  Line {i:02d}: '{line}'")
    print("================================\n")

    data = {
        'raw_text': raw_text,
        'name':      '',
        'job_title': '',
        'company':   '',
        'email':     '',
        'phone':     '',
        'address':   '',
        'website':   '',
    }

    # ── EMAIL ────────────────────────────────────────────────────────────
    email_match = re.search(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', raw_text)
    if email_match:
        data['email'] = email_match.group().strip()

    # ── PHONE ────────────────────────────────────────────────────────────
    for p in re.findall(r'(?:\+?\d{1,3}[\s\-]?)?(?:\(?\d{3,5}\)?[\s\-]?)?\d{3,5}[\s\-]?\d{4,5}', raw_text):
        if len(re.sub(r'\D', '', p)) >= 10:
            data['phone'] = p.strip()
            break

    # ── WEBSITE ──────────────────────────────────────────────────────────
    web_match = re.search(r'(?:https?://|www\.)[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}', raw_text, re.IGNORECASE)
    if web_match:
        data['website'] = web_match.group().strip()

    # ── COMPANY ──────────────────────────────────────────────────────────
    company_keywords = ['pvt', 'ltd', 'llp', 'inc', 'corp', 'solutions',
                        'technologies', 'services', 'consulting', 'systems',
                        'group', 'enterprises', 'industries', 'techwave',
                        'company', 'co.']
    for line in lines:
        if any(kw in line.lower() for kw in company_keywords) and len(line) < 80:
            data['company'] = line.strip()
            break

    # ── JOB TITLE ────────────────────────────────────────────────────────
    title_keywords = ['manager', 'director', 'engineer', 'developer', 'ceo',
                      'cto', 'cfo', 'founder', 'consultant', 'officer',
                      'executive', 'head', 'lead', 'analyst', 'designer',
                      'architect', 'president', 'associate', 'senior',
                      'junior', 'principal', 'vp', 'specialist']
    for line in lines:
        if any(kw in line.lower() for kw in title_keywords) and len(line) < 60:
            cleaned = re.sub(r'[^a-zA-Z\s].*$', '', line).strip()
            data['job_title'] = cleaned
            break

    # ── NAME ─────────────────────────────────────────────────────────────
    skip_words = ['phone', 'email', 'mobile', 'tel', 'fax', 'address',
                  'website', 'www', 'pvt', 'ltd', 'inc', 'corp',
                  'solutions', 'technologies', 'services', 'senior',
                  'junior', 'manager', 'director', 'engineer', 'floor',
                  'road', 'street', 'nagar', 'mumbai', 'delhi', 'pune',
                  'bangalore', 'hyderabad', 'chennai', 'tower', 'complex',
                  'company', 'best', 'logo', 'anywhere', 'techwave']

    already_used = set(filter(None, [
        data['company'].lower().strip(),
        data['job_title'].lower().strip(),
        data['email'].lower().strip(),
        data['website'].lower().strip(),
    ]))

    print("Already used fields:", already_used)

    for line in lines:
        clean = line.strip()
        lower = clean.lower()

        words = clean.split()

        print(f"  Checking name candidate: '{clean}' | words={len(words)}")

        if len(words) < 2 or len(words) > 5:
            print(f"    SKIP: word count {len(words)}")
            continue
        if lower in already_used:
            print(f"    SKIP: already used as another field")
            continue
        if re.search(r'[\d@:/\\+]', clean):
            print(f"    SKIP: contains digit/symbol")
            continue
        if any(w in lower for w in skip_words):
            print(f"    SKIP: contains skip word")
            continue
        if len(clean) < 5 or len(clean) > 40:
            print(f"    SKIP: length {len(clean)}")
            continue
        if all(w[0].isupper() for w in words if len(w) > 1):
            print(f"    ✅ NAME FOUND: '{clean}'")
            data['name'] = clean
            break
        else:
            print(f"    SKIP: not all words capitalized")

    # ── ADDRESS ──────────────────────────────────────────────────────────
    address_keywords = ['floor', 'street', 'st.', 'road', 'rd.', 'avenue',
                        'nagar', 'colony', 'complex', 'tower', 'plot',
                        'sector', 'anywhere', 'bkc', 'bandra', 'kurla',
                        'mumbai', 'delhi', 'bangalore', 'pune', 'hyderabad',
                        'chennai', 'kolkata', 'maharashtra', 'gujarat',
                        'rajasthan', 'karnataka', '400', '110', '560',
                        '500', '600', '12345']
    company_lower = data['company'].lower()
    address_lines = []
    for line in lines:
        lower = line.lower()
        if lower == company_lower:
            continue
        if '@' in line or 'www' in lower or 'http' in lower:
            continue
        if any(kw in lower for kw in address_keywords):
            address_lines.append(line.strip())
    if address_lines:
        data['address'] = ', '.join(address_lines)

    print("Final extracted data:", {k: v for k, v in data.items() if k != 'raw_text'})
    return data