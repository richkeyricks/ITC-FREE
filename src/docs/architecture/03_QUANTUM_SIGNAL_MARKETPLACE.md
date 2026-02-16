# Architecture: Quantum Signal Marketplace (Self-Service)

## 1. Overview
Transforming the Signal Hub from a curated "Admin-Only" list into a **Decentralized Signal Economy**. Professional traders can register as providers automatically, while the platform extracts maximum value through automated fee collection and tier-based scarcity.

## 2. Tier-Based Scarcity Matrix
To maintain signal quality and drive subscription upgrades, the number of "Active Signals" (Pending/Open trades) is strictly capped.

| Tier | Active Signal Slots | Goal |
| :--- | :--- | :--- |
| **STANDARD** | 0 | Consumer Only |
| **GOLD PRO** | 1 Slot | Entry-level Provider |
| **PLATINUM** | 3 Slots | Professional Signalist |
| **INSTITUTIONAL**| 5 Slots | Signal Agency / Team |

## 3. Revenue Engine (The Triple-Fee Model)
The platform ensures profitability at every stage of the signal lifecycle.

### A. Listing Fee (The Anti-Spam Tax)
*   **Cost:** $1.00 (or equivalent IDR) per signal post.
*   **Mechanism:** Deducted from user's "Merchant Wallet" upon clicking 'Broadcast'.
*   **Purpose:** Prevents low-quality signal spamming and generates immediate micro-revenue.

### B. Success Fee (Performance Tax)
*   **Cost:** 30% of Signal Subscription/Access price.
*   **Mechanism:** When a follower pays for access to a provider's channel or specific signal, the platform takes a 30% cut before the remaining 70% hits the provider's wallet.

### C. Usage Fee (Slippage/Volume Tax)
*   **Cost:** $0.10 per copy-trade execution.
*   **Mechanism:** Small tech-fee for using the "Priority Neural Lane" execution engine.

## 4. Automated Vetting (Gatekeeper Logic)
Admin is removed from the loop. The system maintains quality via **Code-Enforced Reputation**:

*   **Audit Engine:** Every signal is tracked by `SignalAuditor`. 
*   **Auto-Suspend:** If a provider's 30-day Win Rate drops below **45%**, their "Broadcast" button is locked for 7 days.
*   **Social Proof:** Providers are ranked in the "Signal Leaderboard" based on Net Pips and Consistency Score.

## 5. Database Schema (Draft)
New table: `marketplace_signals`
*   `id`: UUID
*   `provider_id`: UUID (Link to `user_profiles`)
*   `status`: enum (PENDING, ACTIVE, COMPLETED, SUSPENDED)
*   `access_price`: float (Price set by provider)
*   `metrics_json`: jsonb (Win-rate, Total Pips, Drawdown)
*   `listing_tax_paid`: boolean

---
**Status: PLANNING (Awaiting Implementation)**
**Version: 1.0.0 (Quantum Edition)**
