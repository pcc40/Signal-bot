"""Site-wide settings. Change values here, rebuild, redeploy."""
import os

# --- Change before launch -------------------------------------------------
SITE_URL = "https://eastbridgestrategicpartners.com"   # final domain, no trailing slash
EMAIL = "philip@eastbridgestrategicpartners.com"
PHONE_DISPLAY = "+971 56 744 0057"
PHONE_E164 = "+971567440057"
WHATSAPP = "971567440057"                         # digits only
# True for production. A preview build can switch it off without editing this file:
# EB_INDEXABLE=0 python3 build.py  -> noindex on every page and "Disallow: /" in robots.txt.
# Canonicals, hreflang and SITE_URL are unchanged either way.
INDEXABLE = os.environ.get("EB_INDEXABLE", "1").strip().lower() not in ("0", "false", "no", "off")
PUBLISH_FEES = True  # Approved by the owner on 31 October 2026. True shows the FEES figures on /fees/ and elsewhere
# Home hero film. Keep False until the Vimeo video's privacy setting allows embedding on SITE_URL's
# domain (Vimeo > video > Settings > Privacy > "Where can this be embedded?" > Specific domains).
# While False, the hero shows the photo slideshow only. When True, the film loads on desktop only,
# never with reduced motion or Save-Data, and fades in only once Vimeo reports it is playing.
HERO_VIDEO = False
HERO_VIDEO_VIMEO_ID = "219974514"

# Published fee ranges by level of input, confirmed by the owner on 1 November 2026 (competitor brief, D1).
# Shown only when PUBLISH_FEES is True. Ranges only: never publish a day rate, an hourly rate or a fixed price.
# Every one-off villa is priced against a written scope of works agreed after the free call; work outside
# that scope is quoted before it starts. "range" + " " + "basis" reads as one phrase, e.g. "AED 9,500–15,000 per review".
FEES = {
    "review": {"name": "Review", "range": "AED 9,500–15,000", "basis": "per review"},
    "part": {"name": "Part service", "range": "from AED 28,000", "basis": "a month"},
    "full": {"name": "Full service", "range": "typically 1.75–3%", "basis": "of build cost", "pct": (1.75, 3.0)},
}

def fee_text(level):
    """The published range for one level as a phrase, e.g. "AED 9,500–15,000 per review"."""
    f = FEES[level]
    return f"{f['range']} {f['basis']}"

# --- Business facts --------------------------------------------------------
NAME = "Eastbridge Strategic Partners"
SHORT = "Eastbridge"
LEGAL = "Eastbridge Strategic Partners L.L.C-FZ"
LICENCE = "Meydan Free Zone licence 2540153.01"
LICENCE_NO = LICENCE.rsplit(" ", 1)[-1]
# Coverage policy (owner's direction, 1 November 2026). The area pages are examples, not limits. Worded as a
# policy: never as a claim of existing or past clients or overseas projects.
COVERAGE_INTL = "For clients we represent, we can also support their projects outside the UAE."
COVERAGE = "We cover every community in Dubai and Abu Dhabi. " + COVERAGE_INTL
ADDRESS = {
    "street": "Business Centre, Meydan Grandstand, 6th Floor, Meydan Road",
    "locality": "Nad Al Sheba, Dubai",
    "country": "AE",
    "country_name": "United Arab Emirates",
}
HOURS = "Monday to Friday, 9am–6pm Gulf Standard Time"
# Confirmed by the owner as a firm commitment (31 October 2026). "Working day" follows HOURS.
RESPONSE_PROMISE = "Philip replies personally within one working day"
FOUNDED_TRACK_RECORD_YEARS = 21
SOCIAL = [
    "https://www.instagram.com/eastbridgestrategicpartners/",
]
GA4_ID = "G-120XT9N6XB"          # e.g. "G-XXXXXXX" — leave blank until Google Analytics is set up
GSC_VERIFICATION = "oqg5vPdZKpefhBnXRRASYiH1mD9oZu147uoTHLs313I"  # Google Search Console meta verification code
BING_VERIFICATION = ""
INDEXNOW_KEY = "1d2397b03615846cedbf11228b7285b9"

# Founder — shown on About and as the author of every article
FOUNDER = {
    "name": "Philip Chapman",
    "role": "Founding Partner",
    "company_uk": "P Chapman Construction",
    "company_uk_url": "https://www.pchapmanconstruction.com/",
    # Philip's own public profiles (e.g. his personal LinkedIn URL). Emitted as sameAs in his Person schema.
    # Company pages (Eastbridge's LinkedIn company page, Instagram) go in SOCIAL instead (Organization sameAs).
    "same_as": ["https://www.linkedin.com/in/philip-chapman-757627448/"],
}
