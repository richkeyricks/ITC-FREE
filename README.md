<p align="center">
  <img src="assets/banner.png" alt="ITC +AI Enterprise Banner" width="100%"/>
</p>

<h1 align="center">
  🧠 INTELLIGENCE TELEGRAM COPYTRADE (ITC) +AI
</h1>

<p align="center">
  <strong>Enterprise-Grade Automated Signal Execution Framework with Integrated Artificial Intelligence</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#installation">Installation</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#usage">Usage</a> •
  <a href="#api-reference">API Reference</a> •
  <a href="#cloud-infrastructure">Cloud</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey" alt="Platform"/>
  <img src="https://img.shields.io/badge/MT5-MetaTrader%205-green?logo=metatrader5" alt="MetaTrader 5"/>
  <img src="https://img.shields.io/badge/Telegram-API-blue?logo=telegram" alt="Telegram"/>
  <img src="https://img.shields.io/badge/AI-Multiple%20LLM-purple?logo=openai" alt="AI Powered"/>
  <img src="https://img.shields.io/badge/Cloud-Supabase-darkgreen?logo=supabase" alt="Supabase"/>
  <img src="https://img.shields.io/badge/license-Proprietary-red" alt="License"/>
</p>

---

## 🚀 What is ITC +AI?

**ITC +AI Enterprise** is a cutting-edge, production-ready framework designed for automated trade execution from Telegram signal channels directly into MetaTrader 5. Built with an AI-first architecture, it features intelligent signal parsing, multi-provider LLM fallback, real-time cloud synchronization, and a professional desktop GUI.

> **⚠️ DISCLAIMER:** Trading financial instruments carries significant risk. This software is a tool, not financial advice. Past performance is not indicative of future results.

---

## ✨ Features

| Category | Feature | Description |
|----------|---------|-------------|
| **📡 Signal Processing** | Multi-Channel Monitoring | Subscribe to unlimited Telegram channels simultaneously |
| | Regex + AI Hybrid Parser | Robust signal extraction using pattern matching with LLM fallback |
| | Symbol Normalization | Automatic suffix handling for broker compatibility |
| **🤖 AI Integration** | Multi-Provider Support | OpenRouter, Gemini, Groq with automatic failover |
| | Intelligent Signal Parsing | LLM-powered extraction for non-standard signal formats |
| | AI Chart Analysis | Vision model integration for technical analysis |
| | Personal AI Memory | Cloud-synced conversation history for contextual responses |
| **📈 Trade Execution** | Direct MT5 Integration | Native MetaTrader 5 API connection |
| | Dynamic Lot Sizing | Risk-based calculation or fixed lot modes |
| | Magic Number Isolation | Order identification for multi-EA environments |
| | Emergency Close | One-click position liquidation |
| **🛡️ Risk Management** | Daily Loss Limit | Automatic trading halt on drawdown threshold |
| | Time Filters | Configurable trading hours window |
| | Position Monitoring | Real-time P/L tracking and alerts |
| **🌍 Localization** | Multi-Language Support | Full ID/EN (Indonesian & English) UI switching |
| **☁️ Cloud Infrastructure** | Supabase Backend | Secure PostgreSQL with Row Level Security |
| | Cross-Device Sync | Settings and history available anywhere |
| | Web Dashboard | Mobile-responsive monitoring portal |
| | Admin Panel | Global user management and broadcasting |
| **🎮 Gamification** | Global Leaderboard | Profit and knowledge rankings |
| | Trading Academy | AI-powered quiz system |
| | Achievement Badges | Engagement tracking and rewards |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ITC +AI ENTERPRISE STACK                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   TELEGRAM  │    │  AI ENGINE  │    │   MT5 API   │    │    CLOUD    │  │
│  │    CLIENT   │───▶│   PARSER    │───▶│  EXECUTOR   │    │   BACKEND   │  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
│         │                  │                  │                  │         │
│         ▼                  ▼                  ▼                  ▼         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         CORE APPLICATION                            │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────────────┐   │   │
│  │  │ GUI Layer │ │Config Mgr │ │ Logger    │ │ Session Manager   │   │   │
│  │  └───────────┘ └───────────┘ └───────────┘ └───────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌──────────────┐
                              │  SUPABASE    │
                              │  PostgreSQL  │
                              │  + Auth      │
                              │  + Realtime  │
                              └──────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
              ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
              │  Desktop  │   │    Web    │   │  Mobile   │
              │    App    │   │ Dashboard │   │ (PWA)     │
              └───────────┘   └───────────┘   └───────────┘
```

---

## 📦 Installation

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.10+ | Required for core application |
| MetaTrader 5 | Latest | Must have API access enabled |
| Telegram Account | - | For API credentials |

### Quick Start

```bash
# Clone the repository
git clone https://github.com/richkeyricks/ITC.git
cd ITC

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your credentials

# Run the application
python src/gui.py
```

### Build Executable

```bash
# Build standalone executable
python build_exe.py

# Output: dist/ITC_Plus_AI_Enterprise.exe
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# ═══════════════════════════════════════════
# TELEGRAM CONFIGURATION
# ═══════════════════════════════════════════
TG_API_ID=your_api_id
TG_API_HASH=your_api_hash
TG_CHANNELS=-100xxxxxxxxxx,-100yyyyyyyyyy

# ═══════════════════════════════════════════
# METATRADER 5 CREDENTIALS
# ═══════════════════════════════════════════
MT5_LOGIN=your_login_id
MT5_PASSWORD=your_password
MT5_SERVER=YourBroker-Server

# ═══════════════════════════════════════════
# TRADING PARAMETERS
# ═══════════════════════════════════════════
RISK_PERCENT=1.0
FIXED_LOT=0.01
MAGIC_NUMBER=123456
SYMBOL_SUFFIX=

# ═══════════════════════════════════════════
# AI CONFIGURATION
# ═══════════════════════════════════════════
USE_AI=True
AI_PROVIDER=OpenRouter
AI_API_KEY=sk-or-v1-xxxx

# ═══════════════════════════════════════════
# CLOUD (SUPABASE)
# ═══════════════════════════════════════════
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6...
```

---

## 🔧 Usage

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Signal Parser** | Extracts trading parameters (symbol, direction, entry, TP, SL) from raw text |
| **AI Fallback** | When regex fails, LLM attempts intelligent extraction |
| **Session Manager** | Maintains MT5 connection and handles reconnection |
| **Cloud Sync** | Real-time synchronization of trades, settings, and chat history |

### Signal Format Support

The parser handles multiple signal formats:

```
# Format 1: Standard
BUY XAUUSD
Entry: 2650.00
TP: 2670.00
SL: 2640.00

# Format 2: Compact
SELL EURUSD @ 1.0850 TP 1.0800 SL 1.0900

# Format 3: Natural Language (AI Required)
"Looking to short gold around 2650, target 2620, stop above 2680"
```

### Code Example: Custom Signal Handler

```python
from modules.parser.signal_parser import parse_signal
from modules.mt5.executor import open_trade

# Parse incoming signal
signal = parse_signal(raw_message)

if signal:
    result = open_trade(
        symbol=signal['symbol'],
        order_type=signal['type'],
        entry=signal['entry'],
        tp=signal['tp'],
        sl=signal['sl'],
        lot=calculate_lot(risk_percent=1.0)
    )
    print(f"Trade executed: {result}")
```

---

## 🌐 Cloud Infrastructure

### Database Schema

```sql
-- User Profiles (RLS Enabled)
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hwid TEXT UNIQUE NOT NULL,
    name TEXT,
    email TEXT,
    balance DECIMAL(15,2) DEFAULT 0,
    equity DECIMAL(15,2) DEFAULT 0,
    total_pl DECIMAL(15,2) DEFAULT 0,
    is_pro BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trade History
CREATE TABLE trades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    symbol TEXT NOT NULL,
    type TEXT NOT NULL,
    lot DECIMAL(10,2),
    entry DECIMAL(15,5),
    sl DECIMAL(15,5),
    tp DECIMAL(15,5),
    result TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- AI Chat Memory
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Row Level Security

```sql
-- Users can only see their own data
CREATE POLICY "Users can only access own data"
ON user_profiles FOR ALL
USING (hwid = current_setting('request.jwt.claims')::json->>'sub');
```

---

## 👨‍💻 Developer

<table>
  <tr>
    <td align="center">
      <img src="assets/developer.jpg" width="200" style="border-radius: 50%"/>
      <br/>
      <strong>Richkeyrick</strong>
      <br/>
      <em>Lead Architect & Full-Stack Developer</em>
      <br/><br/>
      <a href="https://github.com/richkeyricks">GitHub</a> •
      <a href="https://saweria.co/richkeyrick">Support</a>
    </td>
  </tr>
</table>

**Technolog Store Dev** — Building intelligent trading solutions since 2024.

---

## 📄 License

This software is **proprietary**. All rights reserved.

- ✅ Personal use permitted
- ❌ Redistribution prohibited
- ❌ Commercial use without license prohibited
- ❌ Reverse engineering prohibited

For licensing inquiries, contact the developer.

---

## 🆘 Support

| Channel | Link |
|---------|------|
| Documentation | [docs/](./docs/) |
| Issues | [GitHub Issues](https://github.com/richkeyricks/ITC/issues) |
| Donation | [Saweria](https://saweria.co/richkeyrick) |

---

<p align="center">
  <strong>ITC +AI Enterprise</strong> — "Intelligence Meets Execution"
</p>

<p align="center">
  <sub>© 2024-2026 Technolog Store Dev. All rights reserved.</sub>
</p>
