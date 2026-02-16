# IMPLEMENTATION PLAN: Proof of Profit (The Truth Engine) 🧬📉

> **MODULE:** Resilience Core
> **VERSION:** 1.0 (Algorithm)
> **SECURITY LEVEL:** INTERNAL (Server-Side Validation)

---

## 1. Goal Description
Implement an algorithmic gatekeeper that prevents "Fake Gurus" from selling presets.
**Rule:** Only presets backed by real trading history with **>5% Profit** (or PF > 1.5) can be listed.

## 2. User Review Required
> [!IMPORTANT]
> **Metric Definition**:
> *   **Win Rate**: (Wins / Total Trades) * 100
> *   **Profit Factor**: Gross Profit / Gross Loss
> *   **Minimum ROI**: 5% Growth on Balance over 7 Days.
> *   **Minimum Trades**: At least 5 trades to prevent "Lucky Shot".

---

## 3. Architecture & Components

### A. Logic: The Validator
*   **Path**: `src/modules/logic/verification_service.py`
*   **Role**:
    1.  `verify_eligibility(user_id)`: Scans `trades` table.
    2.  `calculate_metrics(trades)`: Math engine.
    3.  `mark_as_verified(preset_id, metrics)`: Updates DB.

### B. UI: The Upload Gate
*   **Path**: `src/modules/ui/upload_preset_view.py`
*   **Flow**:
    1.  User clicks "Sell Strategy".
    2.  System runs `verification_service`.
    3.  **Pass**: Shows Listing Form.
    4.  **Fail**: Shows "Not Eligible" Screen with precise reason (e.g., "Profit only 1.2%").

---

## 4. Proposed Changes (Module by Module)

### [MODULE] Logic
#### [NEW] `src/modules/logic/verification_service.py`
*   `VerificationService` Class.
    *   Hardcoded Thresholds (can be moved to config later).
    *   Direct Telemetry Query (Read Only).

### [MODULE] UI
#### [NEW] `src/modules/ui/upload_preset_view.py` (or integrated into `SignalHubView`)
*   Wizard steps: `Verify -> Details -> Price -> Publish`.

---

## 5. Verification Plan
1.  **Mock Test Fail**: Create dummy user with Loss. Verify Rejection.
2.  **Mock Test Pass**: Create dummy user with Profit > 5%. Verify "Verified" Badge.
3.  **Integration**: Ensure `marketplace_presets` table receives the computed `verified_win_rate`.

```python
# Verification Logic Draft
if profit_pct < 5.0 and trades_count < 5:
    raise ValidationException("Not enough proof of profit.")
```
