# Architecture: Strategic Wealth Engine & Merchant Ecosystem

## 1. The Affiliate Wealth Ladder
The system uses a dynamic commission scaling model designed to incentivize high-tier subscriptions.

*   **Logic File:** `affiliate_service.py`
*   **The Multiplier Effect:**
    *   **Level 1 (Gold):** **15%** Commission. 
    *   **Level 2 (Platinum):** **20%** Commission.
    *   **Level 3 (Institutional/Master):** **25%** Commission.
*   **Stealth Attribution:** The "Stealth Referral System" hard-locks a user's invite origin upon their first login, ensuring lifetime commission for the referrer regardless of devicewipe.

## 2. Merchant Bank & Payout Protocol
The infrastructure for users to act as "Strategy Sellers" in the marketplace.

*   **Logic File:** `merchant_service.py`
*   **Revenue Split:** **60% (Seller) / 30% (Platform/Tax) / 10% (Referrer)**.
*   **Payout Rules:**
    *   **Minimum Withdrawal:** Rp 1,000,000.
    *   **Auto-Transfer Window:** Processed every **Friday**.
    *   **Status Tiers:** Platinum/Institutional get "Priority Payout" (faster verification).

## 3. The "Profit Trap" (Anti-Free Mode)
Code-enforced scarcity to drive conversion from Standard to Gold.

*   **Logic File:** `limit_manager.py`
*   **The Trap:**
    *   **Daily Profit Cap:** **$10 USD**. Once reached, the terminal enters "Lockdown" status.
    *   **Trade Limit:** **3 Trades/Day**.
    *   **Account Scope:** Only applies to **REAL** accounts. **DEMO** accounts are unlimited to create a "winning" psychology.

## 4. Gamified Limits (The Academy Bridge)
*   **Logic File:** `education_view.py`
*   **Mechanism:** Users can earn **+3 AI Smart Chats** by achieving 100% on the Daily Quiz.
*   **Purpose:** Keeps users engaged with the platform daily, increasing the exposure to Marketplace ads.

---
**Status: DOCUMENTED**
**Version: 1.0.0 (Strategic Asset)**
