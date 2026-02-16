import os

CHANGELOG_DATA = [
    {
        "version": "v4.9.5",
        "date": "15 Feb 2026",
        "title": "The Telegram Mastery",
        "color": "#06b6d4",
        "updates": [
            "📱 In-App Telegram Login: Native login directly within the app via OTP Popup—no manual API configuration required.",
            "🛡️ Industrial-Grade Copier Engine: A full rewrite of the copier engine with isolated async worker architecture for enterprise reliability.",
            "🔒 Double-Click Guard: Automated protection against rapid start/stop clicks, preventing process duplication and session conflicts.",
            "🧹 Clean Shutdown Protocol: Structured and clean copier termination—no more hanging 'zombie' processes.",
            "⚡ SQLite Session Lock Fix: Intelligent database lock handling when switching between Telegram client modes (Test → Copier).",
            "🔄 Natural Stop Mechanism: Ensures all ongoing async operations complete gracefully before disconnection.",
        ],
        "details": "The most significant update for the Telegram module. Login is now native within the app. The copier engine has been rewritten from scratch with an industrial-grade architecture to eliminate crashes, 'zombie' sessions, and connection conflicts."
    },
    {
        "version": "v4.9.0",
        "date": "14 Feb 2026",
        "title": "The Resilience Core",
        "color": "#ef4444",
        "updates": [
            "📡 Telegram Stability Engine: A complete overhaul of the Telegram connection architecture to prevent sudden disconnections.",
            "🔄 Auto-Recovery Protocol: Automated recovery system (Graceful Reconnect) for Telegram connection losses.",
            "⚡ Thread Safety Upgrade: Enhanced security for multi-threaded operations on the Pyrogram event loop.",
            "🌐 Localization Engine Fix: Resolved crashes in the translation system that affected page loading.",
            "📊 Status Indicator Accuracy: Status indicators for Telegram and MT5 now reflect real-time conditions with 100% accuracy.",
        ],
        "details": "Focused on infrastructure reliability. This update strengthens the Telegram connection foundation and fixes the translation system backbone."
    },
    {
        "version": "v4.8.5",
        "date": "13 Feb 2026",
        "title": "The Precision Update",
        "color": "#f59e0b",
        "updates": [
            "🧠 Intelligence Terminal: Transformation of 'News Center' into 'Intelligence Terminal'—a tactical AI-powered briefing center.",
            "🎯 Interactive Quick Start Stepper: Initial configuration stepper is now interactive for rapid, non-linear navigation.",
            "🔐 Login UI Refinement: Enhanced login page visuals following international standards with ergonomic button layouts.",
            "🎨 Visual Indicator Enhancement: Refined status indicators (Active, Standby, Offline) with a clear 3-state color scheme.",
            "📐 Stepper Visual Polish: Stepper components now use an interactive architecture with dynamic status icons.",
        ],
        "details": "A precision update refining navigation and branding. Intelligence Terminal replaces News Center, and the interactive stepper accelerates setup by 3x."
    },
    {
        "version": "v4.8.0",
        "date": "12 Feb 2026",
        "title": "The Creative Intelligence",
        "color": "#a855f7",
        "updates": [
            "🌐 Multi-Currency Display: Automated currency display (USD price notation for English language).",
            "🤖 AI Creative Studio: AI video prompt generator for professional trading marketing content.",
            "📊 Enhanced Real-Time Signals: Visual improvements to the live signal Leaderboard with motivational messaging.",
            "🛠️ Tab Stability Fix: Resolved crashes in the CTkTabview component due to incompatible parameters.",
            "🌍 Global Ticker Diversity: Updated 70+ ticker names with natural global market representations.",
            "💱 Centralized Currency Engine: A centralized `format_currency()` helper for consistency across all modules.",
        ],
        "details": "A new era of creative intelligence. Features dynamic currency scaling, AI-driven marketing tools, and expanded global ticker diversity."
    },
    {
        "version": "v4.7.5",
        "date": "11 Feb 2026",
        "title": "The Experience Polish",
        "color": "#10b981",
        "updates": [
            "💎 Premium Strategy Showcase: Live previews for premium strategies (Safeguard Scalper, etc.) in the Marketplace.",
            "🗺️ Community-Driven Roadmap: Integrated 'Request & Vote' feature, giving donors control over development direction.",
            "📐 Precision UI Alignment: Visual aesthetic refinements with precision centering in Marketplace and Hall of Fame.",
            "🛠️ Enhanced VPS Integration: Optimized connectivity logic for stable data provider access.",
            "🚀 Optimized Navigation Flow: Reorganized sidebar menu for efficient accessibility of primary features.",
        ],
        "details": "Focused on UX refinement. This update brings higher visual precision, intuitive navigation, and closer community integration."
    },
    {
        "version": "v4.6.0",
        "date": "11 Feb 2026",
        "title": "Core Stability Enhancement",
        "color": "#8b5cf6",
        "updates": [
            "🌉 Connectivity Bridge V2: Enhanced communication architecture between Telegram and MT5 for minimal latency.",
            "🛡️ Network Resilience Protocol: Auto-Reconnect system to maintain trading continuity through network fluctuations.",
            "📊 Smart Data Validation: Multi-layer integrity verification on price feeds for high-accuracy AI analysis.",
            "⚡ Performance Optimization: Core code refactoring for memory efficiency and faster app responsiveness.",
        ],
        "details": "Strengthening the system foundation. Dedicated to under-the-hood performance, ensuring data communication and memory management efficiency."
    },
    {
        "version": "v4.5.0",
        "date": "11 Feb 2026",
        "title": "The Neural Command - Apex Edition",
        "color": "#6366f1",
        "updates": [
            "⚡ Apex Performance Engine: Restored 'Zero-Latency' for ultra-fast signal execution.",
            "📊 Risk Progress Meter: Reactivated 'Daily Loss Meter' (Progress Bar) in the Modern Dashboard.",
            "💳 Midtrans Smart Sense: Integrated intelligent payment flow with self-healing environments.",
            "🛡️ Golden State Recovery: Reconstructed the complete v4 architecture with 100% data integrity.",
            "🎨 UI Polish v4.5: Micro-refinements in 'Quiet Luxury' aesthetics and responsive navigation.",
        ],
        "details": "The Apex edition returns the application to peak performance, restoring all 'Neural Command' features and the real-time risk monitor."
    },
    {
        "version": "v4.4.0",
        "date": "09 Feb 2026",
        "title": "The Neural Command",
        "color": "#fbbf24",
        "updates": [
            "🚀 Command Center v2.0: Transformed the Web Portal into an Institutional Command Center.",
            "🧠 Neural Terminal 2.0: New full-screen chat interface with 'Reasoning Mode' for AI logic visualization.",
            "📡 Live Neural Stream: Live intelligence feed for real-time system activity monitoring.",
            "🛰️ Neural Command Bridge: Integrated unified controls for remote execution synchronization.",
            "🛡️ Modular Shield Architecture: Core system overhaul for military-grade stability and security.",
            "🎨 Aesthetic Overhaul: 'Quiet Luxury' design with optimized Glassmorphism V2 effects.",
        ],
        "details": "A major leap in intelligence and control, transforming the web portal into an institutional instrument with full AI logic transparency."
    },
    {
        "version": "v4.3.0",
        "date": "09 Feb 2026",
        "title": "The Enterprise Integrity",
        "color": "#6366f1",
        "updates": [
            "💳 Institutional Payment Gateway: Full integration with Midtrans Snap via Secure Enclave.",
            "📨 Branded Communication Suite: 'Billionaire Edition' notification emails with full corporate identity.",
            "🛡️ System Integrity Hardening: Enhanced core security and centralized secret management.",
            "⚡ Web-to-App Bridge v2: Optimized license synchronization (Genesis Protocol) between Web and Desktop.",
            "🎨 Visual Precision Fixes: Micro-interaction refinements for the Dashboard and payment portals.",
        ],
        "details": "Focused on enterprise-level integrity, featuring a secure payment gateway and improved corporate communication branding."
    },
    {
        "version": "v4.2.0",
        "date": "09 Feb 2026",
        "title": "The Experience Update",
        "color": "#10b981",
        "updates": [
            "✨ Aurora UI Theme: New visual engine with immersive glassmorphism aesthetics.",
            "📱 Responsive Layout Engine: Optimized dashboard display for various screen resolutions.",
            "📚 ITC Intelligence Hub: Direct access to institutional market research and strategy documentation.",
            "⚡ Unified Access: Seamless synchronization between Web and Desktop access.",
            "📨 Reliability Uplift: Improved notification system stability and core connectivity.",
        ],
        "details": "Focused on user convenience and experience, introducing the 'Aurora' theme and the institutional 'Intelligence Hub'."
    },
    {
        "version": "v4.1.0",
        "date": "29 Jan 2026",
        "title": "The Institutional Edition",
        "color": "#0ea5e9",
        "updates": [
            "🌐 Global Sync 4.1: Multi-Engine Intelligence synchronization.",
            "🏛️ Institutional Transparency: Integrated management authority profiles and E-E-A-T signals.",
            "🛡️ Enterprise Security Shield: Strengthened corporate-grade security infrastructure layers.",
            "🚀 Smart Route Intelligence: Optimized navigation with Smart URL Routing.",
            "💎 Identity Restoration: Restored legendary 'Paper Plane' visuals across the ecosystem.",
            "📖 Rich Knowledge Hub: Integrated global standard smart guides and interactive FAQ.",
        ],
        "details": "Introducing the 'Institutional Edition' standard, focusing on transparency, multi-layered security, and peak performance reliability."
    },
    {
        "version": "v3.3.0",
        "date": "29 Jan 2026",
        "title": "The Visual & Neural Upgrade",
        "color": "#d4af37",
        "updates": [
            "🎨 Billionaire-Grade Landing: Total redesign with 'Deep Black' theme and Bento Grid layout.",
            "🧠 SkyNET Neural Interface: New intelligence module integration with natural responses.",
            "📱 Compact Ecosystem UI: Optimized layout for premium skeuomorphic cards and icons.",
            "⚡ App Launcher Evolution: Vertical scrolling support and navigation refinements.",
            "💬 Chat Experience Polish: Visual cleanup of the input bar and modern response aesthetics.",
        ],
        "details": "Focused on visual perfection and UX. The landing page now meets institutional standards with luxury aesthetics and enhanced AI interaction."
    },
    {
        "version": "v3.2.0",
        "date": "29 Jan 2026",
        "title": "The Neural Intelligence",
        "color": "#d4af37",
        "updates": [
            "🧠 ITC +AI™ Core: Full ecosystem rebranding with 'Neural AI' and 'Intelligence Hub' badges.",
            "📈 Hyper-Speed Charts 4.0: Upgraded rendering engine for zero-latency institutional data.",
            "💳 Enterprise Bridge: Official Snap Payment integration with multi-currency and auto-billing.",
            "📚 Global Authority Content: 'Authority Papers' library for dominant market insights.",
            "✨ Visual Engine v4: 'Billionaire Dark Mode' aesthetics with retina-sharp typography.",
            "🔄 Payment Logic v2: Intelligent billing cycle calculation and subscription management.",
        ],
        "details": "A new era for ITC. Introducing 'Neural AI' as the platform core, supported by institutional market insights and high-performance charting."
    },
    {
        "version": "v3.1.0",
        "date": "28 Jan 2026",
        "title": "The Syndicate Expansion",
        "color": "#d4af37",
        "updates": [
            "🤝 Global Partner Program: 3-Tier partnership system for community expansion.",
            "🌐 Institutional Portal: Public web interface with 'Quiet Luxury' aesthetics.",
            "✅ Certified Strategy Badge: Automated 'Profit & Stability' verification for Marketplace strategies.",
            "⚖️ Legal Framework Core: Integrated institutional standard licenses and disclaimers.",
        ],
        "details": "Expanding the ITC ecosystem to the public. Introducing the partner program and a professional institutional portal."
    },
    {
        "version": "v3.0.0",
        "date": "28 Jan 2026",
        "title": "The Ghost Protocol",
        "color": "#ffd700",
        "updates": [
            "🏆 Ghost Card Ranking: Ultra-modern ranking rows with ITC Gold badges.",
            "🏢 Broker & VPS Specialist: Dedicated technical infrastructure modules in the sidebar.",
            "📏 Ultra-Slim Scrollbars: Sleek 8px navigation with Cyber Blue interaction.",
            "🛡️ Anti-Crash Core 3.0: Global theme stability audit and systemic error handling.",
            "📐 Precision Alignment Logic: Pixel-perfect sidebar menu coordinates.",
            "🚀 Premium Boost Engine: Temporary Pro/VIP upgrades (1-Hour) powered by ITC Coins.",
            "🔐 Unified Vault: Consolidated personal strategies and Marketplace in one hub.",
        ],
        "details": "A major leap in visual fidelity and infrastructure stability, introducing 'Ghost Protocol' for exclusive competition experiences."
    },
    {
        "version": "v2.8.0",
        "date": "28 Jan 2026",
        "title": "The Gravity Economy",
        "color": "#10b981",
        "updates": [
            "💎 Gravity Marketplace: Centralized economic ecosystem for professional trading strategies.",
            "🛡️ Secure Ledger: Bank-grade encrypted financial infrastructure.",
            "🤖 Proof of Profit: Automated strategy quality verification (>5% Win).",
            "🚀 Premium UI: 'Glowing' card designs optimized for user conversion.",
        ],
        "details": "Transforming the ITC economic ecosystem with a verified marketplace and secure financial ledger."
    },
    {
        "version": "v2.7.0",
        "date": "28 Jan 2026",
        "title": "Enterprise Security Core",
        "color": "#e11d48",
        "updates": [
            "🛡️ Enhanced Access 2FA: High-level security through Authenticator integration.",
            "📡 Deep Telemetry: 21+ Real-time parameters (Latency, Drawdown, etc.).",
            "☁️ Cloud Vault: Full encryption for sensitive credential synchronization.",
            "🔄 Zero-Trust Logic: Double verification for all critical access points.",
        ],
        "details": "A massive security upgrade targeting enterprise data integrity through zero-trust architecture."
    },
    {
        "version": "v2.6.0",
        "date": "26 Jan 2026",
        "title": "The Resilience Update",
        "color": "#a855f7",
        "updates": [
            "🛡️ Enterprise Telemetry: Synchronization of 63 hardware and financial parameters.",
            "📡 VIP Broadcaster Pro: 10 Premium presets and Enterprise watermarking.",
            "🛠️ Resilience Engine: More stable cloud synchronization with fallback logic.",
            "💬 Active Communication: Improved chat reply system and message visibility.",
        ],
        "details": "Focused on infrastructure stability and restoring crucial telemetry features for professional traders."
    },
    {
        "version": "v2.5.0",
        "date": "26 Jan 2026",
        "title": "The Ultra Dashboard",
        "color": "#3b82f6",
        "updates": [
            "💎 Ultra Dashboard: Precision alignment through Global Center Offset.",
            "📊 Smart Daily Meter: Custom risk meter with dynamic color responses.",
            "🤖 AI Wellness Toast: Sleek health assistant at the top position.",
            "☁️ Web Monitor 2.0: Synchronized theme button for cloud monitoring.",
        ],
        "details": "Total dashboard overhaul for precision data visualization and distortion-free monitoring."
    },
    {
        "version": "v2.4.0",
        "date": "25 Jan 2026",
        "title": "The Master Broadcaster",
        "color": "#10b981",
        "updates": [
            "📡 MT5 Broadcaster: Automated zero-delay trading broadcast to Telegram.",
            "🛡️ Professional Branding: 'Powered by ITC' Enterprise watermarking.",
            "⚙️ Mode Switcher: Seamless switching between Relay and Broadcast modes.",
            "🚀 Real-time Detection: Automated recognition of Pair, SL, and TP parameters.",
        ],
        "details": "Launching the latest broadcasting engine for professional grade signal distribution directly from MT5."
    },
    {
        "version": "v2.3.0",
        "date": "25 Jan 2026",
        "title": "The Bridge Update",
        "color": "#1f6feb",
        "updates": [
            "💎 VIP System: Exclusive tier for Signal Providers.",
            "🛰️ SPC Hub Bridge: Automated signal relay to whitelabel channels.",
            "🎨 Template Engine: 10 ready-to-use premium presets.",
            "🛒 Preset Marketplace: Sell and share signal designs in the leaderboard.",
            "🔓 PRO vs VIP: Dedicated tiers for AI and business engine features.",
        ],
        "details": "Introducing an economic ecosystem for traders to monetize signal designs and whitelabel channels."
    },
    {
        "version": "v2.2.0",
        "date": "25 Jan 2026",
        "title": "Monetization Update",
        "color": "#f59e0b",
        "updates": [
            "🛰️ Signal Hub: Verified Signal Marketplace.",
            "☁️ ITC Cloud: Integration of Indonesian & Global VPS nodes.",
            "🏆 High-Intel Leaderboard: Real-time performance ranking board.",
            "🏦 Broker Partnership: Recommendations for local (Bappebti) and global brokers.",
        ],
        "details": "Focused on broker and server integration for minimal latency execution."
    },
    {
        "version": "v1.0.0",
        "date": "1 Jan 2026",
        "title": "Initial Release",
        "color": "#2ea44f",
        "updates": [
            "🚀 Initial Release - ITC +AI",
            "📱 Telegram to MT5 Copytrade",
            "🤖 AI Trading Assistant",
        ],
        "details": "The birth of the Intelligence Telegram Copytrade ecosystem."
    }
]

def generate_release_md(entry):
    version = entry['version']
    date = entry.get('date', 'Unknown Date')
    title = entry.get('title', 'Release Update')
    updates = entry['updates']
    details = entry.get('details', '')
    
    # Correct filename for Pro version
    zip_name = f"ITC_PRO_AI_Trading_Assistant_{version}.zip"
    
    md_content = f"""<p align="center">
  <img src="../assets/banner.png" alt="ITC +AI Enterprise Logo" width="100%"/>
</p>

# 🚀 {title} {version} ({date})
"""
    if title != 'Release Update':
        md_content += f"""
**INTELLIGENCE TELEGRAM COPYTRADE (ITC) +AI**
*Official Production Build - {title}*
"""
    else:
        md_content += f"""
**INTELLIGENCE TELEGRAM COPYTRADE (ITC) +AI**
*Official Production Build*
"""
    
    if details:
        md_content += f"\n{details}\n"

    md_content += f"""
### ⚡ {title} Updates
"""
    for update in updates:
        md_content += f"*   {update}\n"
        
    md_content += f"""
### 📦 Installation
1.  **Download** the [**{zip_name}**](https://github.com/richkeyricks/ITC-FREE/releases/download/{version}/{zip_name}) below.
2.  **Extract** to your preferred high-performance directory.
3.  **Run** the executable inside the package.
4.  No Python installation required.

[**Download Release {version} ZIP**](https://github.com/richkeyricks/ITC-FREE/releases/download/{version}/{zip_name})

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
    return md_content

# Create output directory
output_dir = r"c:\APLIKASI YANG DIBUAT\TELEGRAM MT5\temp_itc_free\releases"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Generate files
for entry in CHANGELOG_DATA:
    filename = f"{entry['version']}.md"
    filepath = os.path.join(output_dir, filename)
    content = generate_release_md(entry)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated: {filename}")
