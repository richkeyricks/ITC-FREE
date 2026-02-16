# CHECKLIST: Proof of Profit (Verification Engine)

## 📅 Pre-Flight (Documentation)
- [x] Implementation Plan created (`docs/modules/05_PROOF_OF_PROFIT_PLAN.md`)
- [ ] Review `marketplace_presets` schema (Is `verified_win_rate` present?).

## 🛠️ Code Implementation (Execution)
### Logic (Verification Layer)
- [ ] Create `src/modules/logic/verification_service.py`
- [ ] Implement `calculate_metrics(trades)`
- [ ] Implement `verify_eligibility(user_id)` -> Returns (Boolean, Reason)

### UI (Seller Flow)
- [ ] Create `src/modules/ui/upload_preset_view.py`
- [ ] Step 1: Pre-Check (Run Verification Service).
- [ ] Step 2: Show "Verified Badge" or "Rejection Notice".
- [ ] Step 3: Input Form (Title, Price, Description).
- [ ] Step 4: Upload to Supabase.

### Integration
- [ ] Add "Sell Strategy" button to `SignalHub` or `Marketplace` (Navigation).

## 🛡️ Verification
- [ ] **Test**: Upload Fails for New Account (No History).
- [ ] **Test**: Upload Succeeds for Account with >5% Profit (Mock).
- [ ] **Audit**: Ensure Metrics are populated in DB.

## ✅ Finalization
- [ ] Update `CHANGELOG.md`.
- [ ] Mark Checklist as **APPLIED**.
