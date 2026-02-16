# IMPLEMENTATION PLAN: The Wealth Dashboard (Merchant 2.0) 📊👑

> **MODULE:** Financial Nucleus
> **VERSION:** 1.0 (UI/UX)
> **SECURITY LEVEL:** CLASSIFIED (Read-Only Telemetry)

---

## 1. Goal Description
Create a "Banking-Grade" Dashboard for sellers to view their Wealth.
The goal is **ADDICTION** (Dopamine Hits) and **TRUST** (Transparency).

**Key Metrics to Display:**
1.  **Balance Active** (Liquid Cash).
2.  **Balance Pending** (Escrow).
3.  **Life-time Earnings** (The Vanity Metric).
4.  **Sales Graph** (Visual Progress).

## 2. User Review Required
> [!NOTE]
> **No Chart Library**: We will use a custom Canvas-based drawing engine (Simple Bars) to keep dependencies low (no matplotlib heavyweight).
> **Data Source**: Direct Read from `user_wallets` and `marketplace_orders` (via RLS).

---

## 3. Architecture & Components

### A. Logic: The Ledger Reader
*   **Path**: `src/modules/logic/merchant_service.py`
*   **Role**:
    *   `get_wallet_balance()`: Returns Active/Pending/Lifetime.
    *   `get_sales_history(days=7)`: Returns data for the chart.
    *   `request_payout(amount, bank_details)`: Inserts to `payout_requests`.

### B. UI: The Wealth View
*   **Path**: `src/modules/ui/merchant_dashboard_view.py`
*   **Design**:
    *   **Top Card**: "TOTAL BALANCE" (Huge Green Font).
    *   **Chart Area**: "Weekly Performance" (Neon Bars).
    *   **Action Bar**: "WITHDRAW FUNDS" (Golden Button).
    *   **History Table**: List of recent sales.

### C. Router
*   **Integration**: Add to `Sidebar` (Navigation) -> "Merchant Bank".

---

## 4. Proposed Changes (Module by Module)

### [MODULE] Logic
#### [NEW] `src/modules/logic/merchant_service.py`
*   `MerchantService` class. 
*   **Security**: Fetches only user's own data (RLS enforced on DB side).

### [MODULE] UI
#### [NEW] `src/modules/ui/merchant_dashboard_view.py`
*   `MerchantDashboardView(ctk.CTkFrame)`
*   Custom `draw_chart()` method using `ctk.CTkCanvas`.

### [MODULE] Config
#### [UPDATE] `src/modules/ui/navigation_panel.py`
*   Add Icon/Button for "Merchant Area".

---

## 5. Verification Plan
1.  **Mock Data Verification**: Populate DB with dummy sales.
2.  **Visual Test**: Check if Green Numbers "Glow".
3.  **Functional Test**: Click "Withdraw" -> Check `payout_requests` table.

```python
# Test Query
wallet = db_manager.fetch("user_wallets", {"user_id": my_id})
print(wallet['balance_active']) # Should match Dashboard
```
