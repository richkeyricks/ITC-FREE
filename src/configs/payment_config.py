# ══════════════════════════════════════════════════════════════════════════════
# 💳 PAYMENT CONFIGURATION
# 🎯 ROLE: Centralized configuration for Midtrans Payment Gateway
# ══════════════════════════════════════════════════════════════════════════════

# --- CREDENTIALS (SANDBOX) ---
# Provided by User for Testing/Trial
MERCHANT_ID = ""
CLIENT_KEY  = ""
SERVER_KEY  = ""

# --- ENDPOINTS ---
IS_PRODUCTION = False

BASE_URL_SANDBOX = "https://app.sandbox.midtrans.com/snap/v1/transactions"
BASE_URL_PRODUCTION = "https://app.midtrans.com/snap/v1/transactions"

CORE_API_SANDBOX = "https://api.sandbox.midtrans.com/v2"
CORE_API_PRODUCTION = "https://api.midtrans.com/v2"

API_URL = BASE_URL_PRODUCTION if IS_PRODUCTION else BASE_URL_SANDBOX
STATUS_BASE_URL = CORE_API_PRODUCTION if IS_PRODUCTION else CORE_API_SANDBOX

# --- HEADERS ---
# Basic Auth Header is generated dynamically in service, but we define content-type here
DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# --- REDIRECTS (ENTERPRISE BRIDGE) ---
# Phantom Page hosted on Vercel to handle 3DS close loop
VERCEL_PROJECT_URL = "https://itc-global-app.vercel.app" 
REDIRECT_STATUS_PAGE = f"{VERCEL_PROJECT_URL}/payment_status.html"
