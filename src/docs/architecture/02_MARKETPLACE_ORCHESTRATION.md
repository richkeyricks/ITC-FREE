# 🏦 GRAVITY ECONOMY: ORCHESTRATION BLUEPRINT

> **STATUS:** ARCHITECTURAL STANDARD
> **MODULE:** Financial Ecosystem & Marketplace
> **SECURITY LEVEL:** CLASSIFIED (See Security Protocol)

---

## 1. CORE PHILOSOPHY: TRUST & ADDICTION

### The "Proof of Profit" Verify-Gate 🛡️
*   **Problem**: Unverified strategies degrade marketplace trust.
*   **Solution**: Strategies are **LOCKED** until "Resilience Core" (Telemetry) validates >5% Profit/Week.
*   **Effect**: "The Holy Grail" marketplace perception.

### The "Wealth Dashboard" Hook 📊
*   **Metric 1**: "Today's Earnings" (Green/Huge).
*   **Visual**: Revenue Analytics Chart (Dopamine Hit).
*   **Metric 2**: "Passive Impact" (Active Copiers).
*   **Interaction**: Frictionless Payout Button.

---

## 2. SECURITY ARCHITECTURE: "ZERO-TRUST & IDEMPOTENCY"

### Zero-Knowledge Payment Flow
1.  **Client**: Request `CreateTransaction` -> Edge Function.
2.  **Edge Function**:
    *   Validate User Session (RLS).
    *   **Idempotency Check**: Prevent double-billing using unique `order_id`.
    *   Retrieve `PAYMENT_GATEWAY_TOKEN` (Server-Side Only).
    *   Request Snap Token from Provider.
3.  **Client**: Render Embedded Payment View (WebView/QRIS).
4.  **Webhook**: Provider -> Edge Function -> `UpdateWallet`.
    *   **Auto-Unlock**: Immediate trigger to `purchased_presets` table.

> **RULE**: NO API KEYS in Client Code.

---

## 3. DATABASE SCHEMA: "THE DOUBLE-ENTRY LEDGER"

### A. Inventory (`marketplace_presets`)
*   `id`: UUID
*   `proof_stats`: JSONB (WinRate, Drawdown, ProfitFactor)
*   `is_verified`: Boolean

### B. Transactions (`marketplace_orders`) & (`transaction_logs`)
*   `order_id`: UUID (Midtrans ID - Primary Key for Idempotency)
*   `status`: ENUM ('PENDING', 'PAID', 'FAILED')
*   `amount`: DECIMAL
*   `log_data`: JSONB (Audit Trail for "Financial Nucleus" - Zero Trust)

### C. Banking (`user_wallets`)
*   `balance_active`: DECIMAL (Liquid/Withdrawable)
*   `balance_pending`: DECIMAL (Escrow 3-Day Hold for Fraud Prevention)
*   `affiliate_earnings`: DECIMAL (Recurring 10%)

---

## 4. MONEY FLOW & VIRAL GROWTH (Affiliate 2.0)

### Seller Journey
1.  **Monetize**: User selects Preset -> System checks `proof_stats` -> Listed.
2.  **Earn**: Sales credit `balance_pending`.
3.  **Release**: T+3 Days -> Moves to `balance_active`.
4.  **Payout**: Request -> Admin Dashboard -> Manual/Auto Transfer via Gateway.

### Affiliate System (Creating an Army)
1.  **Direct Link**: Share Preset Link -> Commission.
2.  **Application Referral**: "Cookie-Based" tracking.
    *   **10% Recurring**: Lifetime commission from referred users' subscriptions.
    *   **Goal**: Users promote the app *for* us.

### Buyer Journey
1.  **Discover**: Filter by "Profit Factor > 2.0".
2.  **Unlock**: Payment Popup (QRIS/VA) -> Idempotency Check.
3.  **Deploy**: Instant Logic Injection into MT5.

---

## 5. AUDIT & COMPLIANCE
*   **Treasury View ("The Nucleus")**: Admin panel showing GMV (Gross Market Value) & Platform Fees.
*   **Institutional Fee**: 10% Fee for Standard users, 0% for Institutional (forcing upgrades).
*   **Dispute Resolution**: Escrow buffer allows refunding "Broken" strategies before Seller withdrawal.
