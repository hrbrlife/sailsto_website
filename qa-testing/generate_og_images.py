#!/usr/bin/env python3
"""
OG Image Generator v2 — All HRBR Properties

Usage:
    # Generate all sites (requires OPENROUTER_API_KEY env var):
    OPENROUTER_API_KEY=sk-or-... python3 qa-testing/generate_og_images.py

    # Generate specific sites only:
    OPENROUTER_API_KEY=sk-or-... python3 qa-testing/generate_og_images.py --sites sailsto kyclat

    # Available site names: sailsto, kyclat, hrbr, melusina

Prerequisites:
    pip install requests Pillow

Screenshots:
    Site screenshots are stored in qa-testing/screenshots/brand_*.png
    To refresh them, capture new screenshots and place them there.

How it works:
    1. Sends site screenshot to AI (Gemini Flash) for context-aware background generation
    2. Crops/resizes AI output to exactly 1200x630
    3. Composites real brand logos (never AI-generated logos)
    4. Adds page titles via PIL text rendering
    5. Saves to each site's static/public directory
"""

import argparse, requests, json, base64, io, os, sys, time
from PIL import Image, ImageDraw, ImageFont

# -- Config --
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
API_KEY = os.environ.get('OPENROUTER_API_KEY', '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')
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.5-flash-image"
W, H = 1200, 630
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')

FONT_PATH = next((p for p in [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
] if os.path.exists(p)), None)

FONT_REG_PATH = next((p for p in [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
] if os.path.exists(p)), None)


def font(size, bold=True):
    p = FONT_PATH if bold else FONT_REG_PATH
    return ImageFont.truetype(p, size) if p else ImageFont.load_default()


def img_to_b64(path, max_dim=768):
    img = Image.open(path).convert('RGB')
    img.thumbnail((max_dim, max_dim), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"


def call_ai(prompt, screenshot_path=None):
    """Call AI with optional screenshot context. Returns PIL Image or None."""
    content = []
    if screenshot_path and os.path.exists(screenshot_path):
        content.append({"type": "image_url", "image_url": {"url": img_to_b64(screenshot_path)}})
    content.append({"type": "text", "text": prompt})

    for attempt in range(3):
        try:
            r = requests.post(API_URL, headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }, json={
                "model": MODEL,
                "messages": [{"role": "user", "content": content}],
                "max_tokens": 8192,
                "response_format": {"type": "image"}
            }, timeout=120)
            if r.status_code != 200:
                print(f"    API {r.status_code}, retry {attempt+1}")
                time.sleep(3); continue
            imgs = r.json().get('choices', [{}])[0].get('message', {}).get('images', [])
            if imgs:
                b64 = imgs[0]['image_url']['url'].split(',')[1]
                return Image.open(io.BytesIO(base64.b64decode(b64))).convert('RGB')
            print(f"    No image returned, retry {attempt+1}")
            time.sleep(2)
        except Exception as e:
            print(f"    Error: {e}, retry {attempt+1}")
            time.sleep(3)
    return None


def fit_to_og(img):
    """Resize + center-crop to exactly 1200x630."""
    ratio_target = W / H
    ratio_img = img.width / img.height
    if ratio_img > ratio_target:
        new_h, new_w = H, int(ratio_img * H)
    else:
        new_w, new_h = W, int(W / ratio_img)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - W) // 2
    top = (new_h - H) // 2
    return img.crop((left, top, left + W, top + H))


def darken(img, amount=0.3):
    return Image.blend(img, Image.new('RGB', (W, H), (0, 0, 0)), amount)


def paste_logo(bg, logo_path, max_h=180, y_offset=-30):
    """Paste real logo centered on background, preserving alpha."""
    logo = Image.open(logo_path).convert('RGBA')
    r = min(max_h / logo.height, (W * 0.5) / logo.width)
    logo = logo.resize((int(logo.width * r), int(logo.height * r)), Image.LANCZOS)
    x = (W - logo.width) // 2
    y = (H - logo.height) // 2 + y_offset
    bg = bg.convert('RGBA')
    bg.paste(logo, (x, y), logo)
    return bg.convert('RGB')


def centered_text(img, text, y, size=36, color=(255, 255, 255), bold=True):
    draw = ImageDraw.Draw(img)
    f = font(size, bold)
    bbox = draw.textbbox((0, 0), text, font=f)
    x = (W - (bbox[2] - bbox[0])) // 2
    draw.text((x, y), text, fill=color, font=f)
    return img


# -- SAILS.TO --

def do_sailsto():
    logo = os.path.join(REPO_ROOT, 'hugo-site', 'static', 'sail_logo_w.png')
    shot = os.path.join(SCREENSHOTS_DIR, 'brand_sailsto.png')
    out = os.path.join(REPO_ROOT, 'hugo-site', 'static')

    pages = {
        'og-image.png':       ('Hybrid Securities Infrastructure', ''),
        'og-brokers.png':     ('For Brokers', 'Expand your offerings with CrossSecurities'),
        'og-investors.png':   ('For Investors', 'Access institutional-grade CrossSecurities'),
        'og-pricing.png':     ('Pricing', 'Transparent CrossSecurities pricing'),
        'og-how-it-works.png':('How It Works', 'CrossSecurities infrastructure explained'),
        'og-about.png':       ('About Us', 'Building CrossSecurities infrastructure'),
        'og-issuers.png':     ('For Issuers', 'Issue bonds, shares, and RWA tokens'),
        'og-introducers.png': ('For Introducers', 'Earn referral commissions'),
        'og-institutions.png':('For Institutions', 'Institutional-grade infrastructure'),
        'og-compare.png':     ('Compare', 'How Sails.to stacks up'),
        'og-compliance.png':  ('Compliance', 'Built-in regulatory compliance'),
        'og-security.png':    ('Security', 'Multi-layer security architecture'),
        'og-oversight.png':   ('Oversight', 'Transparent governance'),
        'og-signup.png':      ('Sign Up', 'Get started with Sails.to'),
        'og-trustees.png':    ('For Trustees', 'Trust services for CrossSecurities'),
        'og-players.png':     ('Key Players', 'Ecosystem participants'),
        'og-platform.png':    ('Platform', 'The Sails.to issuance platform'),
        'og-faq.png':         ('FAQ', 'Frequently asked questions'),
        'og-roadmap.png':     ('Roadmap', 'What we are building next'),
        'og-knowledge.png':   ('Knowledge Base', 'Learn about CrossSecurities'),
        'og-contact.png':     ('Contact', 'Get in touch with us'),
        'og-legal.png':       ('Legal', 'Terms and regulatory information'),
    }

    print("\n[sails.to] Generating background from site screenshot...")
    bg = call_ai(
        "This is a screenshot of sails.to, a fintech securities platform. "
        "Generate a subtle, minimal abstract background image that matches "
        "this website's dark navy/charcoal aesthetic. Think: soft dark gradient "
        "with very faint geometric lines or light mesh, like a premium fintech hero. "
        "NO text, NO logos, NO icons, NO UI elements. Just a clean dark background. "
        "Landscape orientation, wider than tall (about 2:1 ratio).",
        shot
    )
    if bg is None:
        print("  Fallback to solid bg")
        bg = Image.new('RGB', (W, H), (13, 17, 28))
    else:
        bg = fit_to_og(bg)
    bg = darken(bg, 0.25)

    for fname, (title, sub) in pages.items():
        img = bg.copy()
        img = paste_logo(img, logo, max_h=150, y_offset=-50)
        if sub:
            img = centered_text(img, title, H - 135, size=36)
            img = centered_text(img, sub, H - 88, size=22, color=(190, 195, 210), bold=False)
        else:
            img = centered_text(img, title, H - 100, size=28, color=(190, 195, 210), bold=False)
        img.save(f'{out}/{fname}')
        print(f"  {fname}")


# -- KYC.LAT --

def do_kyclat():
    shot = os.path.join(SCREENSHOTS_DIR, 'brand_kyclat.png')
    out = os.path.join(REPO_ROOT, 'kyclat_website', 'public')

    print("\n[kyc.lat] Generating background from site screenshot...")
    bg = call_ai(
        "This is a screenshot of kyc.lat, a compliance/KYC platform. "
        "Generate a subtle, minimal abstract background that matches this site's "
        "dark slate-blue aesthetic. Soft gradients, maybe very faint circuit-board "
        "or network-node lines in a slightly lighter blue. Premium, understated, corporate. "
        "NO text, NO logos, NO icons. Just a clean dark background. "
        "Landscape orientation, about 2:1 ratio.",
        shot
    )
    if bg is None:
        bg = Image.new('RGB', (W, H), (15, 23, 42))
    else:
        bg = fit_to_og(bg)
    bg = darken(bg, 0.2)

    img = bg.copy()
    img = centered_text(img, 'kyc.lat', H // 2 - 45, size=58)
    img = centered_text(img, 'Sovereign Self-Hosted KYC/AML Platform', H // 2 + 30, size=24, color=(160, 190, 220), bold=False)

    for name in ['og-image.png', 'twitter-card.png']:
        img.save(f'{out}/{name}')
        print(f"  {name}")


# -- HRBR.LIFE --

def do_hrbr():
    shot = os.path.join(SCREENSHOTS_DIR, 'brand_hrbr.png')
    out = os.path.join(REPO_ROOT, 'hrbrlife_website')

    print("\n[hrbr.life] Generating background from site screenshot...")
    bg = call_ai(
        "This is a screenshot of hrbr.life, a company portfolio site with a bold "
        "yellow (#f5c518) and black color scheme. Generate a subtle abstract background "
        "that matches: mostly black/very dark charcoal with a hint of warm gold/amber "
        "gradient or glow, like a subtle light leak. Understated and editorial. "
        "NO text, NO logos, NO icons, NO geometric shapes. Just atmosphere. "
        "Landscape orientation, about 2:1 ratio.",
        shot
    )
    if bg is None:
        bg = Image.new('RGB', (W, H), (17, 17, 17))
    else:
        bg = fit_to_og(bg)
    bg = darken(bg, 0.15)

    img = bg.copy()
    img = centered_text(img, 'HRBR.LIFE', H // 2 - 40, size=56, color=(245, 197, 24))
    img = centered_text(img, 'Harbour Life', H // 2 + 30, size=28, color=(230, 230, 225), bold=False)

    img.save(f'{out}/og-image.png')
    print(f"  og-image.png")


# -- MELUSINA-OS.ORG --

def do_melusina():
    logo = os.path.join(REPO_ROOT, 'hugo-site', 'static', 'melulogoimage.png')
    shot = os.path.join(SCREENSHOTS_DIR, 'brand_melusina.png')
    out = os.path.join(REPO_ROOT, 'INSTAKYCAPP_WEBSITE', 'public')

    print("\n[melusina-os.org] Generating background from site screenshot...")
    bg = call_ai(
        "This is a screenshot of melusina-os.org, a sovereign operating system. "
        "Generate a subtle, minimal abstract background matching this dark purple/indigo "
        "tech theme. Soft dark gradient, maybe very faint hexagonal mesh or subtle "
        "aurora-like glow in deep purple/blue. Very understated and premium. "
        "NO text, NO logos, NO icons. Just a clean dark background. "
        "Landscape orientation, about 2:1 ratio.",
        shot
    )
    if bg is None:
        bg = Image.new('RGB', (W, H), (18, 15, 35))
    else:
        bg = fit_to_og(bg)
    bg = darken(bg, 0.25)

    img = bg.copy()
    if os.path.exists(logo):
        img = paste_logo(img, logo, max_h=170, y_offset=-40)
    img = centered_text(img, 'The Operating System You Actually Own', H - 90, size=24, color=(190, 190, 210), bold=False)

    for name in ['og-image.png', 'twitter-card.png']:
        img.save(f'{out}/{name}')
        print(f"  {name}")


SITE_FUNCS = {
    'sailsto': do_sailsto,
    'kyclat': do_kyclat,
    'hrbr': do_hrbr,
    'melusina': do_melusina,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate OG images for HRBR properties')
    parser.add_argument('--sites', nargs='+', choices=list(SITE_FUNCS.keys()),
                        default=list(SITE_FUNCS.keys()),
                        help='Sites to generate (default: all)')
    args = parser.parse_args()

    print("=" * 50)
    print("OG Image Generator v2")
    print(f"Sites: {', '.join(args.sites)}")
    print("=" * 50)

    for site in args.sites:
        SITE_FUNCS[site]()

    print("\n" + "=" * 50)
    print("DONE -- all images 1200x630")
    print("=" * 50)
