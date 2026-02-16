# IMPLEMENTATION PLAN: Secure Payment Gateway (Midtrans) 🛡️💳

> **MODULE:** Financial Nucleus
> **VERSION:** 1.0 (Integration)
> **SECURITY LEVEL:** CRITICAL (Zero-Leak)

---

## 1. Goal Description
Implement a secure, "Zero-Knowledge" payment flow using Midtrans Snap API. The Python Client must **NEVER** touch the Server Key. All transaction signing happens in a secure, serverless environment.

## 2. User Review Required (Safety Checks)
> [!IMPORTANT]
> **Midtrans Server Key**: You must supply the `SB-Mid-server-XXXX` key.
> **Deployment**: We will deploy a Supabase Edge Function `payment-gateway`.

---

## 3. Architecture & Components

### A. Backend: The Secure Token Signer (Edge Function)
*   **Path**: `supabase/functions/payment-gateway/index.ts`
*   **Role**:
    1.  Receives JWT + Metadata from Python App.
    2.  Signs transaction with `MIDTRANS_SERVER_KEY`.
    3.  Returns `token` (Snap Token) and `redirect_url`.
*   **Security**: Runs in Deno V8 sandbox. Key restricted to ENV vars.

### B. Frontend: The Payment View (Python/CTk)
*   **Path**: `src/modules/ui/payment_view.py`
*   **Role**:
    1.  Renders WebView (CustomTkinter integration or external browser flow).
    2.  Polls transaction status (or listens to realtime table updates).
*   **Style**: "Glowing" Checkout with Countdown Timer.

### C. Logic: The Bridge
*   **Path**: `src/modules/logic/payment_service.py`
*   **Role**: Handles Edge Function invocation and database transaction record creation.

---

## 4. Proposed Changes (Module by Module)

### [MODULE] Logic (Business Layer)
#### [NEW] `src/modules/logic/payment_service.py`
*   `class PaymentService`:
    *   `create_transaction(amount, dataset)`: Calls Edge Function.
    *   `verify_payment(order_id)`: Checks status via Cloud.

### [MODULE] UI (Presentation Layer)
#### [NEW] `src/modules/ui/payment_view.py`
*   `class PaymentView(ctk.CTkToplevel)`:
    *   Embedded WebView (if feasible) or QR Code display.
    *   "Waiting for Payment" Pulsing Animation.

### [MODULE] Config & Types
#### [MODIFY] `src/constants/api_endpoints.py`
*   Add `EDGE_FUNCTION_URL`.

---

## 5. Verification Plan
1.  **Mock Test**: Call Edge Function with `curl`.
2.  **UI Test**: Open Payment View, verify Snap Token generation.
3.  **End-to-End**: Scan QRIS (Sandbox), verify `balance_pending` increases in DB.

```bash
# Verification Command (Example)
curl -X POST https://PROJECT_ID.supabase.co/functions/v1/payment-gateway -H "Authorization: Bearer USER_JWT"
```
