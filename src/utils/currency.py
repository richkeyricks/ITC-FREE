# src/utils/currency.py
# ══════════════════════════════════════════════════════════════════════════════
# 💱 CENTRALIZED CURRENCY FORMATTER
# 🎯 ROLE: Dynamic currency formatting based on APP_LANGUAGE
# 📌 RULE: ID → Rupiah (Rp), EN → US Dollar ($)
# ══════════════════════════════════════════════════════════════════════════════

import os

# --- CONSTANTS ---
IDR_TO_USD_RATE = 15500  # Approximate conversion rate

# --- HELPERS ---

def is_english():
    """Check if app is running in English mode."""
    return os.getenv("APP_LANGUAGE", "ID") != "ID"

def get_currency_symbol():
    """Returns currency symbol based on APP_LANGUAGE."""
    return "$" if is_english() else "Rp"

def format_currency(amount_idr, force_idr=False):
    """
    Formats amount (stored in IDR) to localized currency string.
    
    Args:
        amount_idr: Amount in Indonesian Rupiah (all DB values are stored in IDR)
        force_idr: If True, always display as IDR regardless of language
    
    Returns:
        Formatted string like "Rp 1,500,000" or "$96.77"
    """
    if force_idr or not is_english():
        return f"Rp {amount_idr:,.0f}"
    else:
        usd = amount_idr / IDR_TO_USD_RATE
        if usd >= 1:
            return f"${usd:,.2f}"
        elif usd > 0:
            return f"${usd:,.4f}"
        else:
            return "$0"

def get_per_referral_value():
    """Returns per-referral income estimate in local currency unit (raw number)."""
    return 10 if is_english() else 150000  # $10 or Rp 150,000

def format_per_referral_estimate(count):
    """
    Returns formatted estimated income string for wealth simulator.
    
    Args:
        count: Number of referrals
    """
    if is_english():
        est = count * 10  # $10 per referral
        return f"Est: ${est:,.0f} / mo"
    else:
        est = count * 150000  # Rp 150,000 per referral
        return f"Est: Rp {est:,.0f} / mo"

def get_min_withdraw_text():
    """Returns minimum withdrawal text in local currency."""
    if is_english():
        return "Enter Amount (Min $7):"
    else:
        return "Enter Amount (Min Rp 100.000):"

def get_min_withdraw_error():
    """Returns minimum withdrawal error message."""
    if is_english():
        return "Minimum withdrawal is $7"
    else:
        return "Minimum withdrawal is Rp 100.000"

def get_earnings_guide_texts():
    """Returns earnings guide bullet points."""
    if is_english():
        return [
            "• Commission: Your share of profit from invited users.",
            "• Fee: $0. Being a partner is 100% FREE.",
            "• Payout: Request anytime (Min $7)."
        ]
    else:
        return [
            "• Commission: Your share of profit from invited users.",
            "• Fee: Rp 0. Being a partner is 100% FREE.",
            "• Payout: Request anytime (Min Rp 100k)."
        ]
