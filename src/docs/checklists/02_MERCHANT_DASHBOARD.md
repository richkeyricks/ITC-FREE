# CHECKLIST: Merchant Dashboard (The Wealth Nucleus)

## 📅 Pre-Flight (Documentation)
- [x] Implementation Plan created (`docs/modules/04_MERCHANT_DASHBOARD_PLAN.md`)
- [ ] Review `SECURITY_PROTOCOL.md` (Ensure Read-Only Policy for Wallet Data).

## 🛠️ Code Implementation (Execution)
### Logic (Service Layer)
- [ ] Create `src/modules/logic/merchant_service.py`
- [ ] Implement `get_wallet_balance` (DB Query).
- [ ] Implement `get_sales_history` (DB Query).
- [ ] Implement `request_payout` (Insert `payout_requests`).

### UI (Presentation Layer)
- [ ] Create `src/modules/ui/merchant_dashboard_view.py`
- [ ] Implement "Glowing Number" Component.
- [ ] Implement "Revenue Chart" (Canvas Drawing).
- [ ] Implement "Withdraw" Modal Dialog.

### Navigation
- [ ] Update `src/modules/ui/navigation_panel.py` -> Add "Merchant" Button.
- [ ] Update `src/gui.py` -> Register Router.

## 🛡️ Verification
- [ ] **Test**: Dashboard loads without crash.
- [ ] **Test**: Dummy data renders correct "Green" balance.
- [ ] **Test**: Withdraw button creates DB entry.

## ✅ Finalization
- [ ] Update `CHANGELOG.md`.
- [ ] Mark Checklist as **APPLIED**.
