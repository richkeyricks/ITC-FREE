# ══════════════════════════════════════════════════════════════════════════════
# 🌐 API ENDPOINTS & CONFIGURATION
# 🏠 CENTRALIZED CONSTANTS (Single Source of Truth)
# ══════════════════════════════════════════════════════════════════════════════

# --- EDGE FUNCTIONS (SUPABASE) ---
# Replace 'YOUR_PROJECT_ID' with actual Project ID during deployment
EDGE_FUNCTION_BASE = "https://YOUR_PROJECT_ID.supabase.co/functions/v1"

EDGE_FUNCTION_URL = f"{EDGE_FUNCTION_BASE}/payment-gateway"
SNAPSHOT_API = f"{EDGE_FUNCTION_BASE}/snapshot"

# --- TELEMETRY ---
TELEMETRY_ENDPOINT = f"{EDGE_FUNCTION_BASE}/telemetry-ingest"

# --- MARKETPLACE ---
MARKETPLACE_API = f"{EDGE_FUNCTION_BASE}/marketplace"

# --- WEB & AFFILIATE ---
WEB_BASE_URL = "https://telegramcopytrade.vercel.app"
REGISTER_URL = f"{WEB_BASE_URL}/register"
