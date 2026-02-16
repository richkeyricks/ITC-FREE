# ITC +AI ENTERPRISE: MASTER FEATURE MATRIX 🧠🛰️

**Document Classification:** PUBLIC / CLIENT-FACING
**Version:** 4.1.0 (Institutional Edition)
**Scope:** Full Application Ecosystem (Technical + Commercial)

---

## 1. CORE EXECUTION MODULE (The Engine) ⚙️
*The foundational layer responsible for connecting Telegram signals to MetaTrader 5 with zero-latency precision.*

### A. Universal Signal Bridge
- **Multi-Channel listening:** Simultaneously monitor unlimited Telegram channels (Private & Public) without conflict.
- **Regex + AI Hybrid Parser:**
    - **Standard Mode:** Instantly recognizes formats like *"BUY XAUUSD @ 2000 TP 2010 SL 1990"*.
    - **Natural Language Mode:** Understands unstructured chats like *"Emas valid buy sekarang, target pendek aja"*.
- **Symbol Normalization:** Automatically adjusts signal symbols (e.g., `XAUUSD`) to match broker-specific suffixes (e.g., `XAUUSD.pro`, `Gold_micro`).
- **Magic Number Isolation:** Assigns unique IDs to trades, preventing conflict with other EAs running on the same account.

### B. Execution Logic
- **Pending Order Handling:** Automatically converts "Buy Limit" / "Sell Stop" signals into valid MT5 pending orders.
- **Update/Modification Support:**
    - **"Move SL to BE":** Detects instruction to move Stop Loss to Break Even.
    - **"Close Half":** Supports partial closing of positions.
    - **"Delete Pending":** Removes pending orders if the signal provider cancels them.
- **Gap Protection:** Prevents entry if price has moved too far from the signal's entry point (configurable slippage).

---

## 2. NEURAL INTELLIGENCE LAYER (The Brain) 🧠
*The AI subsystem that elevates ITC from a simple copier to a smart trading assistant.*

### A. AI Signal Filter (Vision & Text)
- **Chart Validation (Vision AI):** Analyzes image attachments in signals. If a chart looks bearish but the signal is BUY, the AI flags it as "Low Probability".
- **News Bias Filter:** Scans global sentiment before executing. If High Impact News (NFP/FOMC) is imminent, it pauses execution.
- **Scam/Spam Detection:** Automatically filters out marketing messages, spam, or fake signals using Context Analysis.

### B. ITC Neural Assistant (Cloudflare Llama 3)
- **Institutional Concierge:** A dedicated CS chatbot embedded in the Web Dashboard.
- **Deep Knowledge Matrix:** Provides real-time guidance on platform usage and strategy logic.
- **Contextual Memory:** Remembers previous user queries for a fluid conversation flow.

---

## 3. SOVEREIGN RISK GUARDIAN (The Shield) 🛡️
*Institutional-grade capital protection modules designed to prevent catastrophic loss.*

### A. Capital Protection
- **Equity Hard-Stop:** Automatically disables all trading if equity drops below a specific % (e.g., "Stop if Equity < $9,000").
- **Max Daily Loss:** Limits the maximum allowable loss per day. Once hit, the system locks until server reset (00:00).
- **Drawdown Limiter:** Monitors floating drawdown in real-time. Can be set to "Close All" if drawdown exceeds X%.

### B. Position Sizing
- **Dynamic Risk %:** Calculates lot size based on Account Balance and Stop Loss distance (e.g., "Risk 1% per trade").
- **Fixed Lot Mode:** Forces a specific lot size for all trades (e.g., 0.01 lot).

---

## 4. GLOBAL CLOUD ECOSYSTEM (The Network) ☁️
*The web-based infrastructure that keeps the user connected and synchronized.*

### A. Web Dashboard (Vercel)
- **Real-Time Traffic:** View visitor stats and global user activity.
- **Leaderboard System:** Global ranking of top performing ITC users.
- **Signal Bridge View:** Web-based interface to monitor signals processed by the desktop app.

### B. The Alpha Syndicate (Community)
- **Private Network:** Exclusive access to the ITC Discord/Telegram community.
- **Whale Alerts:** (Web) Real-time feed of institutional large-cap movements.

---

## 5. MEMBERSHIP TIERS & PRICING 💎
*Current subscription structure designed for every level of trader.*

| TIER LEVEL | MONTHLY | YEARLY (Save 20%) | LIFETIME |
| :--- | :--- | :--- | :--- |
| **STANDARD (Free)** | **GRATIS ($0)** | **GRATIS ($0)** | **GRATIS ($0)** |
| **GOLD (Pro)** | **$29** (Rp 450k) | **$279** (Rp 4.3jt) | **$899** (Rp 13.9jt) |
| **PLATINUM (VIP)** | **$99** (Rp 1.5jt) | **$950** (Rp 14.7jt) | **$2,499** (Rp 38.7jt) |
| **INSTITUTIONAL** | **$299** (Rp 4.6jt) | **$2,990** (Rp 46.3jt) | **N/A** (Contract Only) |

---

## 6. FEATURE COMPARISON MATRIX 📊
*Granular breakdown of capabilities per tier.*

| Feature / Capability | STANDARD (Free) | GOLD (Pro) | PLATINUM (VIP) | INSTITUTIONAL |
| :--- | :--- | :--- | :--- | :--- |
| **1. AI Assistant Limit** | 3 Msgs/Day | 100 Msgs/Day | 250 Msgs/Day | 500 Msgs/Day |
| **2. Copy Trade Limit** | **5x Trade / Day** | Unlimited | Unlimited | Unlimited |
| **3. Execution Mode** | Telegram Parse | Telegram Parse | **+ Alpha Copy** | **+ Whitelabel** |
| **4. Max Channels** | 1 Channel | 5 Channels | 20 Channels | **Unlimited** |
| **5. AI Tech Analysis** | **2x / Day** | ✅ Fully Unlocked | ✅ Fully Unlocked | ✅ Fully Unlocked |
| **6. Relay Bridge (SPC)** | 🔒 Locked | 🔒 Locked | ✅ **Active** | ✅ **Whitelabel** |
| **7. Marketplace Access** | Buy Only | Buy & Mint | Buy, Mint, Sell | Preferred Seller |
| **8. Polling Speed** | 30s (Basic) | 5s (Standard) | 1s (Fast) | **0.5s (HFT)** |
| **9. Risk Guard** | Manual | Basic Cutloss | Trailing DD | Institutional |
| **10. Support** | Community | Knowledge Base | Priority Ticket | Personal Chat |

### Detailed Explanation of Limits:
*   **Copy Trade Limit:** The Free Tier handles up to 5 signals per day perfectly. To trade 24/7 without missing opportunities, an upgrade is required.
*   **Polling Speed:** Higher tiers perform "HFT-grade" checks (up to 0.5s), ensuring you enter trades ahead of the crowd (slippage reduction).
*   **Max Channels:** Free users focus on 1 signal provider. Institutional users can monitor the entire market (Unlimited).

---

## 7. ECOSYSTEM ECONOMY (TAX & FEES) ⚖️
*Transparency on how the ITC Marketplace and Profit Sharing works.*

### A. Profit Sharing (Success Fee)
*Applies only when you use "Copy Trade Leader" features.*
- **Concept:** You (Follower) only pay when you profit.
- **High-Water Mark (HWM):** We never charge fees during drawdown/recovery. You only pay on **Net New Profit**.
- **Rate:** Varies by Master Trader setting (typically 20-30%).

### B. Marketplace Sales Fee
*Applies to Creators selling Preset/Strategies.*
- **Standard Fee:** 20% (Platinum Users)
- **Reduced Fee:** 10% (Institutional Users)
- **Note:** This fee covers server maintenance, payment gateway costs, and marketing.

---

## 8. DOCUMENTATION & SUPPORT 📚
- **Interactive Knowledge Hub:** Full FAQ and usage guides available on the web.
- **Smart Troubleshooting:** The app detects errors (e.g., "Invalid Token") and provides "Self-Heal" suggestions.
- **Localization:** Full support for **Indonesian** and **English** (one-click switch).

---

## 9. FORENSIC & CYBER-INTELLIGENCE (The Eye) 🛰️
*Advanced tracking and identity verification modules to secure the ecosystem and detect bad actors.*

### A. Digital DNA & Hardware Profiling (Tier-GOD)
- **Biological Hardware Signature:** Unmaskable identity tracking using Canvas, WebGL, and AudioContext artifacts (independent of IP/Cookies).
- **Environmental Super-Sensors:** Real-time monitoring of target Battery Level (%), Power Status, and Media Device counts (Cam/Mic/Spk).
- **Hardware Deep-Scan:** Accurate detection of GPU Renderer, CPU Core clusters, RAM capacity, and Screen Refresh Rate.

### B. Network Signal Intelligence (Level 6)
- **High-Fidelity Geo-Forensics:** Location tracking down to the **District (Kecamatan)** and **Locality (Kelurahan)** level.
- **Signal Side-Channels:** Real-time STUN Latency (RTT), Downlink speed tracking, and Connection Type detection (4G/WiFi/Ethernet).
- **Security Mask Evasion:** Advanced detection of VPN, Proxy, Tor, and known Data Center/Hosting providers.
- **Abuse Contact Database:** Automated retrieval of ISP abuse emails and ASN ownership history.

---

**CONFIDENTIALITY NOTICE:**
*Proprietary administration modules, arbitrage logic, and internal security protocols are excluded from this public document.*
