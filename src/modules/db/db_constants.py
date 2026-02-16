# src/modules/db/db_constants.py
"""
Database Constants - Centralized & Protected
Gravity Rule 1: All constants in one place, never hardcoded elsewhere.

This file should NEVER be modified during feature changes.
Only modify when database schema changes.
"""

# --- TABLE NAMES ---
TABLE_USER_PROFILES = "user_profiles"
TABLE_ENTITLEMENTS = "entitlements"
TABLE_MARKETPLACE_ORDERS = "marketplace_orders"
TABLE_MARKETPLACE_PRESETS = "marketplace_presets"
TABLE_AFFILIATE_CODES = "affiliate_codes"
TABLE_AFFILIATE_REFERRALS = "affiliate_referrals"
TABLE_AFFILIATE_COMMISSIONS = "affiliate_commissions"
TABLE_TRADES = "trades"
TABLE_ACTIVITY_LOGS = "activity_logs"
TABLE_CHAT_LOGS = "chat_logs"
TABLE_SYSTEM_CONFIG = "system_config"
TABLE_SYSTEM_LOGS = "system_logs"
TABLE_USER_CHANNELS = "user_channels"
TABLE_DONATIONS = "donations"
TABLE_USER_WALLETS = "user_wallets"
TABLE_PAYOUT_REQUESTS = "payout_requests"

# --- COLUMN SETS (For validation) ---
MARKETPLACE_ORDER_COLUMNS = [
    'order_id', 'buyer_id', 'preset_id', 'preset_name', 
    'amount_gross', 'platform_fee', 'amount_net', 
    'status', 'payment_method', 'snap_token', 
    'fraud_status', 'redirect_url'
]

USER_PROFILE_COLUMNS = [
    'hwid', 'email', 'name', 'phone', 'country', 
    'subscription_tier', 'premium_until', 
    'is_pro', 'ai_quota', 'ai_total_requests',
    'is_banned', 'created_at', 'updated_at'
]

# --- TIER DEFINITIONS ---
TIER_FREE = "free"
TIER_STANDARD = "standard"
TIER_GOLD = "gold"
TIER_PLATINUM = "platinum"
TIER_INSTITUTIONAL = "institutional"

VALID_TIERS = [TIER_FREE, TIER_STANDARD, TIER_GOLD, TIER_PLATINUM, TIER_INSTITUTIONAL]

# --- ERROR MESSAGES (Localized) ---
ERROR_DB_NOT_CONNECTED = "DB not connected"
ERROR_NO_ENTITLEMENT = "Email ini belum memiliki lisensi ITC. Silakan beli akses di telegramcopytrading.com"
ERROR_INVALID_CREDENTIALS = "Email atau Password salah!"
ERROR_USER_ALREADY_EXISTS = "Email sudah terdaftar. Silakan login."
