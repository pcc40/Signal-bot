"""Site-wide settings. Change values here, rebuild, redeploy."""

# --- Change before launch -------------------------------------------------
SITE_URL = "https://www.eastbridgepartners.ae"   # final domain, no trailing slash
EMAIL = "enquiries@eastbridgepartners.ae"
PHONE_DISPLAY = "+971 56 744 0057"
PHONE_E164 = "+971567440057"
WHATSAPP = "971567440057"                         # digits only
INDEXABLE = True     # False adds noindex everywhere (use for a staging deploy)
PUBLISH_FEES = False # True shows the fee figures in FEES below on /fees/
# Home hero film. Keep False until the Vimeo video's privacy setting allows embedding on SITE_URL's
# domain (Vimeo > video > Settings > Privacy > "Where can this be embedded?" > Specific domains).
# While False, the hero shows the photo slideshow only. When True, the film loads on desktop only,
# never with reduced motion or Save-Data, and fades in only once Vimeo reports it is playing.
HERO_VIDEO = False
HERO_VIDEO_VIMEO_ID = "219974514"

# Proposed fee figures — only shown when PUBLISH_FEES is True. Set them yourself.
FEES = {
    "plot_review": "AED 9,500",
    "rescue_review": "AED 15,000",
    "monthly_from": "AED 28,000",
    "percent_band": "1.75%–3%",
}

# --- Business facts --------------------------------------------------------
NAME = "Eastbridge Strategic Partners"
SHORT = "Eastbridge"
LEGAL = "Eastbridge Strategic Partners L.L.C-FZ"
LICENCE = "Meydan Free Zone licence 2540153.01"
ADDRESS = {
    "street": "Business Centre, Meydan Grandstand, 6th Floor, Meydan Road",
    "locality": "Nad Al Sheba, Dubai",
    "country": "AE",
    "country_name": "United Arab Emirates",
}
HOURS = "Monday to Friday, 9am–6pm Gulf Standard Time"
# Softened to an aim until the owner confirms one working day as an operational commitment (review brief, section 4).
RESPONSE_PROMISE = "Philip aims to reply personally within one working day"
FOUNDED_TRACK_RECORD_YEARS = 21
SOCIAL = [
    "https://www.instagram.com/eastbridgestrategicpartners/",
]
GA4_ID = ""          # e.g. "G-XXXXXXX" — leave blank until Google Analytics is set up
GSC_VERIFICATION = ""  # Google Search Console meta verification code
BING_VERIFICATION = ""
INDEXNOW_KEY = "1d2397b03615846cedbf11228b7285b9"

# Founder — shown on About and as the author of every article
FOUNDER = {
    "name": "Philip Chapman",
    "role": "Founding Partner",
    "company_uk": "P Chapman Construction",
    "company_uk_url": "https://www.pchapmanconstruction.com/",
}
