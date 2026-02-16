"""
ITC Partner Data Constants
Centralized configuration for all partner/affiliate links.
Following Gravity Rules: No magic strings, centralized constants.
"""

# --- TYPES ---
from typing import TypedDict, List, Optional

class PartnerItem(TypedDict):
    name: str
    desc: Optional[str]
    desc_id: Optional[str]
    desc_en: Optional[str]
    url: str
    icon: str
    featured: Optional[bool]
    is_featured: Optional[bool] # Backwards compatibility

# --- CONSTANTS ---

# Forex Brokers (Official & Partners)
FOREX_BROKERS: List[PartnerItem] = [
    {
        "name": "Exness (Global)",
        "desc_id": "🌍 Spread ultra-rendah, WD instan. Pilihan utama untuk scalper!",
        "desc_en": "🌍 Ultra-low spreads, instant withdrawals. Top choice for scalpers!",
        "url": "https://one.exnessonelink.com/a/7siaufj122?source=app",
        "icon": "🔥",
        "featured": True
    },
    {
        "name": "MIFX (Indonesia)",
        "desc_id": "🇮🇩 Terregulasi Bappebti. Support lokal, deposit IDR instan.",
        "desc_en": "🇮🇩 Bappebti Regulated. Local support, instant IDR deposit.",
        "url": "https://client.mifx.com/r/itc",
        "icon": "🏆",
        "featured": True
    },
    {
        "name": "Vantage Markets",
        "desc_id": "🌐 Raw ECN spreads, support MT4/MT5, tersedia copy trading.",
        "desc_en": "🌐 Raw ECN spreads, MT4/MT5 support, copy trading available.",
        "url": "https://www.vantagemarkets.com/forex-trading/forex-trading-account/?utm_source=promo&utm_medium=social&utm_campaign=RAF&utm_term=NA&utm_content=NA&c=BO0JMa/J63gBYluWnJLINQ==",
        "icon": "⚡",
        "featured": True
    }
]

# VPS Providers (Official & Partners)
VPS_PROVIDERS: List[PartnerItem] = [
    {
        "name": "HOSTINGER (RECOMMENDED)",
        "desc_id": "👑 Pilihan #1 Trader Pro. Uptime 99.99%, Server Jakarta/SG. Bonus Domain Gratis.",
        "desc_en": "👑 #1 Choice for Pro Traders. 99.99% Uptime. Free Domain. Best Value.",
        "url": "https://www.hostinger.com/id/vps/forex-hosting?REFERRALCODE=6WJRICHKE8SN",
        "icon": "⭐",
        "featured": True,
        "recommended": True, # Triggers Yellow Highlight Badge
        "color": "yellow" # Custom UI Hint
    },
    {
        "name": "SocialVPS (Forex Special)",
        "desc_id": "🚀 Latency <2ms ke Jakarta. Support QRIS/BCA. Wajib untuk Scalper.",
        "desc_en": "🚀 Ultra low latency. Local payment support. Must have for Scalpers.",
        "url": "https://client.socialvps.net/aff.php?aff=4871",
        "icon": "🔥",
        "featured": True
    },
    {
        "name": "IdCloudHost",
        "desc_id": "☁️ Cloud Stabil & Murah. Bayar per jam (Pay-as-you-go).",
        "desc_en": "☁️ Stable & Affordable Cloud. Pay-as-you-go supported.",
        "url": "https://my.idcloudhost.com/aff.php?aff=19307",
        "icon": "🏆",
        "featured": True
    },
    {
        "name": "Vultr (International)",
        "desc_id": "⚡ VPS performa tinggi, data center global, deploy instan.",
        "desc_en": "⚡ High-performance VPS, global data centers, instant deploy.",
        "url": "https://www.vultr.com/?ref=9865859",
        "icon": "🌐",
        "featured": True
    }
]

# Payment Gateways
PAYMENT_GATEWAYS: List[PartnerItem] = [
    {
        "name": "Wise",
        "desc": "💸 Best for international transfers. Low fees, real exchange rate.",
        "url": "https://wise.com/invite/dic/trickyhusnyt",
        "icon": "🌐",
        "is_featured": True
    },
    {
        "name": "CoinPayments",
        "desc": "₿ Accept 2000+ cryptocurrencies. Multi-coin wallet included.",
        "url": "https://www.coinpayments.net/index.php?ref=be5558decbd7fc478a03b4ac84ba1101",
        "icon": "🪙",
        "is_featured": False
    },
]

# Stock/Investment Platforms
STOCK_PLATFORMS: List[PartnerItem] = [
    {
        "name": "GotTrade",
        "desc": "🇺🇸 Trade US stocks fractionally. Start from $1. Zero commission.",
        "url": "https://heygotrade.com/referral?code=838474",
        "icon": "📈",
        "is_featured": True
    },
    {
        "name": "Ajaib",
        "desc_id": "🇮🇩 Saham Indonesia & Reksa Dana. Terdaftar OJK. User-friendly.",
        "desc_en": "🇮🇩 Indonesian Stocks & Mutual Funds. OJK Registered. User-friendly.",
        "url": "https://login.ajaib.co.id/sign-up/?referral-code=rick5181485733",
        "icon": "📊",
        "is_featured": True
    },
]

# Copy Trading Platforms
COPY_TRADE_PLATFORMS: List[PartnerItem] = [
    {
        "name": "NAGA Global",
        "desc": "🤖 Social trading network. Copy top traders automatically.",
        "url": "https://naga-global.com/register?refcode=ipdlbr",
        "icon": "🦎",
        "is_featured": True
    },
    {
        "name": "TraderWagon",
        "desc": "🚃 Copy trade crypto on Binance. Automated portfolio mirroring.",
        "url": "https://www.traderwagon.com/lander?oref=https%3A%2F%2Fbit.ly%2FCopyTradeBinance&ref=zoh4qio",
        "icon": "🔄",
        "is_featured": False
    },
]

# Crypto Exchanges
CRYPTO_EXCHANGES: List[PartnerItem] = [
    {
        "name": "Binance",
        "desc": "🌍 World's largest crypto exchange. Low fees, high liquidity.",
        "url": "https://accounts.binance.me/id/register?ref=190820790",
        "icon": "₿",
        "is_featured": True
    },
    {
        "name": "Indodax",
        "desc": "🇮🇩 #1 Indonesia crypto exchange. IDR pairs, local support.",
        "url": "https://indodax.com/register?ref=tricky",
        "icon": "🇮🇩",
        "is_featured": True
    },
    {
        "name": "Bybit",
        "desc": "⚡ Derivatives & spot trading. Up to 100x leverage.",
        "url": "https://www.bybit.com/en-US/invite?ref=XVY3MB%230",
        "icon": "🚀",
        "is_featured": True
    },
    {
        "name": "Tokocrypto",
        "desc": "🇮🇩 Binance-backed Indonesian exchange. Fast IDR deposit.",
        "url": "https://www.tokocrypto.com/account/signup?ref=B19Q335W",
        "icon": "🏪",
        "is_featured": False
    },
    {
        "name": "Huobi",
        "desc": "🌏 Global exchange with Asian focus. Wide altcoin selection.",
        "url": "https://www.huobi.mk/id-id/topic/double-invite/register/?invite_code=qzq24223&name=Banshee&avatar=4&inviter_id=11343840",
        "icon": "🔥",
        "is_featured": False
    },
]

# Category Definitions for UI (Bilingual)
PARTNER_CATEGORIES_ID = [
    ("💳", "PAYMENT GATEWAY", PAYMENT_GATEWAYS),
    ("📈", "SAHAM & INVESTASI", STOCK_PLATFORMS),
    ("🤖", "COPY TRADE", COPY_TRADE_PLATFORMS),
    ("₿", "CRYPTO EXCHANGE", CRYPTO_EXCHANGES),
]

PARTNER_CATEGORIES_EN = [
    ("💳", "PAYMENT GATEWAY", PAYMENT_GATEWAYS),
    ("📈", "STOCKS & INVESTMENT", STOCK_PLATFORMS),
    ("🤖", "COPY TRADE", COPY_TRADE_PLATFORMS),
    ("₿", "CRYPTO EXCHANGE", CRYPTO_EXCHANGES),
]

# Legacy fallback
PARTNER_CATEGORIES = PARTNER_CATEGORIES_EN
