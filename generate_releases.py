import os
import sys

# Ensure we can import from src
sys.path.insert(0, os.path.abspath("src"))

from constants.changelog_data import CHANGELOG_DATA

TEMPLATE_HEADER = """<p align="center">
  <img src="../assets/banner.png" alt="ITC +AI Enterprise Logo" width="100%"/>
</p>

# 🚀 {title} {version} ({date})

**INTELLIGENCE TELEGRAM COPYTRADE (ITC) +AI**
*Official Production Build - {title}*

"""

TEMPLATE_FOOTER = """
### 📦 Installation
1.  **Download** the [**ITC_ProMax_AI_Trading_Assistant_{version}.zip**](https://github.com/richkeyricks/ITC-FREE/releases/download/{version}/ITC_ProMax_AI_Trading_Assistant_{version}.zip) below.
2.  **Extract** to your preferred high-performance directory.
3.  **Run** the executable inside the package.
4.  No Python installation required.

[**Download Release {version} ZIP**](https://github.com/richkeyricks/ITC-FREE/releases/download/{version}/ITC_ProMax_AI_Trading_Assistant_{version}.zip)

> *Built from Technolog Store - Richkeyrick Dev. Powered by Haineo AI OS Lab Network Vision AI.*

---

## 💎 Secure Your Lifetime Enterprise License

Looking for the full Apex experience without recurring subscriptions? Unlock the complete institutional-grade suite including unlimited AI reasoning and multi-channel synchronization:

*   **Official Marketplace (Exclusive Offer):** [**Technolog Store (Shopee)**](https://shopee.co.id/MT4-MT5-ITC-AI-Telegram-CopyTrade-MT5-%E2%80%93-Aplikasi-Copy-Trading-Otomatis-Tercanggih-Telegram-ke-MT5-AI-Assistant-Trading-Respon-Super-Cepat-Tanpa-Subscription-Lifetime-Auto-Save-check-Signal-Tanya-Jawab-AI-i.34185939.43523268382?extraParams=%7B%22display_model_id%22%3A306892759583%2C%22model_selection_logic%22%3A3%7D&sp_atk=4201bdd1-b43a-4366-bdad-186e53835bb2&xptdk=4201bdd1-b43a-4366-bdad-186e53835bb2) — *Direct Access & Region-Specific Discounts.*
*   **Global Intelligence Portal:** [**TelegramCopyTrading.com**](https://Tekegramcopytrading.com) — *World-Class Support & Instant Activation.*

> [!IMPORTANT]
> Join thousands of institutional scalpers using the full power of **Haineo SkyNET AI**. Professional results demand professional tools.

---

## 🤝 Support the Development

**ITC +AI Enterprise** is the result of thousands of hours of research, development, and AI training. It is provided for **free** to empower the retail trading community.

### 💖 Ways to Support
1.  **Star this Repo** ⭐
2.  **Donate**:
    - [Saweria](https://saweria.co/richkeyrick) (Local Support ID/QRIS)
    - [PayPal](https://www.paypal.com/paypalme/richkeyrick)
    - [Ko-fi](https://ko-fi.com/richkeyrick)
3.  **Share**: Post your profit screenshots on social media!

> *"Innovation is expensive, but community support is priceless."* — **Richkeyrick**
"""

OUTPUT_DIR = "temp_itc_free/releases"

def generate_releases():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    for release in CHANGELOG_DATA:
        version = release["version"]
        filename = f"{version}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Build Body
        body = f"{release.get('details', '')}\n\n"
        
        # Build Updates List
        if release.get("updates"):
            body += f"### ⚡ {release['title']} Updates\n"
            for update in release["updates"]:
                body += f"*   {update}\n"
        
        # Combine
        full_content = TEMPLATE_HEADER.format(
            title=release["title"],
            version=version,
            date=release["date"]
        )
        full_content += body
        full_content += TEMPLATE_FOOTER.format(version=version)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
            
        print(f"Generated: {filepath}")

if __name__ == "__main__":
    generate_releases()
