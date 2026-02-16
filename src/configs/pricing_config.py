
# Gravity ITC +AI Pricing Configuration
# Strictly follows Master Matrix v2.7.0

TIER_ORDER = ["STANDARD", "GOLD", "PLATINUM", "INSTITUTIONAL"]

CYCLES = {
    "MONTHLY": {"label": "BULANAN", "code": "mo", "discount": ""},
    "YEARLY": {"label": "TAHUNAN", "code": "yr", "discount": "HEMAT 20%"},
    "LIFETIME": {"label": "SEUMUR HIDUP", "code": "life", "discount": "BEST VALUE"}
}

PRICING_MATRIX = {
    "STANDARD": {
        "display_name": "STANDARD",
        "tagline": "The Hook",
        "color": "#52525b", # Zinc 600
        "glow_color": "",
        "prices": {
            "MONTHLY": 0,
            "YEARLY": 0,
            "LIFETIME": 0
        },
        "idr_prices": {
            "MONTHLY": "GRATIS",
            "YEARLY": "GRATIS",
            "LIFETIME": "GRATIS"
        },
        "features": [
            "✅ Basic Telemetry",
            "✅ Manual Trading",
            "✅ 3 AI Chats / Day",
            "❌ No Marketplace Access",
            "❌ No Cloud Backup"
        ],
        "cta": "CURRENT PLAN",
        "cta_color": "#3f3f46",
        "scarcity_enabled": False
    },
    "GOLD": {
        "display_name": "GOLD PRO",
        "tagline": "The Cashflow Engine",
        "color": "#eab308", # Yellow 500
        "glow_color": "#ca8a04",
        "prices": {
            "MONTHLY": 29,
            "YEARLY": 279,
            "LIFETIME": 899
        },
        "idr_prices": {
            "MONTHLY": "Rp 450.000",
            "YEARLY": "Rp 4.300.000",
            "LIFETIME": "Rp 13.900.000"
        },
        "features": [
            "✅ Unlimited AI & Copy Trade",
            "✅ 5 Signal Channels",
            "✅ Basic Equity Guard",
            "✅ Mint Own Presets",
            "✅ Priority Support"
        ],
        "cta": "UPGRADE GOLD",
        "cta_color": "#eab308", # Gold
        "reasons": "Perfect for serious retail traders targeting daily cashflow.",
        "scarcity_enabled": True,
        "scarcity_type": "FLASH", # Early Bird
        "badge_text": "EARLY BIRD QUOTA"
    },
    "PLATINUM": {
        "display_name": "PLATINUM VIP",
        "tagline": "The Whale Filter",
        "color": "#3b82f6", # Blue 500
        "glow_color": "#2563eb",
        "prices": {
            "MONTHLY": 99,
            "YEARLY": 950,
            "LIFETIME": 2499
        },
        "idr_prices": {
            "MONTHLY": "Rp 1.500.000",
            "YEARLY": "Rp 14.700.000",
            "LIFETIME": "Rp 38.700.000"
        },
        "features": [
            "🔥 Alpha Copy (Machine Code)",
            "🔥 SPC Relay Bridge",
            "🔥 20 Signal Channels",
            "🔥 Marketplace Seller Access",
            "🔥 1s Polling Speed"
        ],
        "cta": "BECOME VIP",
        "cta_color": "#3b82f6",
        "reasons": "For professional traders who need speed and marketplace access.",
        "scarcity_enabled": True,
        "scarcity_type": "GENESIS",
        "badge_text": "GENESIS PROTOCOL"
    },
    "INSTITUTIONAL": {
        "display_name": "INSTITUTIONAL",
        "tagline": "The Boss (B2B)",
        "color": "#a855f7", # Purple 500
        "glow_color": "#9333ea",
        "prices": {
            "MONTHLY": 299,
            "YEARLY": 2990,
            "LIFETIME": None # N/A for Lifetime
        },
        "idr_prices": {
            "MONTHLY": "Rp 4.600.000",
            "YEARLY": "Rp 46.300.000",
            "LIFETIME": "CONTRACT ONLY"
        },
        "features": [
            "👑 Whitelabel Reports",
            "👑 0.5s Thunder Execution",
            "👑 Lowest Fees (10%)",
            "👑 Unlimited Signals",
            "👑 Private Dedicated Node"
        ],
        "cta": "CONTACT SALES",
        "cta_color": "#a855f7",
        "reasons": "Infrastructure for Fund Managers managing >$100k.",
        "scarcity_enabled": True,
        "scarcity_type": "FOUNDER",
        "badge_text": "FOUNDER'S ALLOCATION"
    }
}
