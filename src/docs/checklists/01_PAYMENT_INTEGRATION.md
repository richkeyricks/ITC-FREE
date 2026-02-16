# CHECKLIST: Secure Payment Gateway (Midtrans)

## 📅 Pre-Flight (Documentation)
- [x] Implementation Plan created (`docs/modules/03_PAYMENT_GATEWAY_PLAN.md`)
- [ ] Backup existing `src` (Manual Copy)
- [ ] Ensure `SECURITY_PROTOCOL.md` is reviewed.

## 🛠️ Code Implementation (Execution)
### Backend (Edge Function)
- [ ] Create `supabase/functions/payment-gateway/index.ts`
- [ ] Implement `Deno.serve` with CORS headers.
- [ ] Add Midtrans Snap API Logic (`fetch` call).
- [ ] Set Environment Variables (`MIDTRANS_SERVER_KEY`) in Cloud.

### Frontend (Python)
- [ ] Create `src/modules/logic/payment_service.py` (API Bridge).
- [ ] Create `src/modules/ui/payment_view.py` (Checkout UI).
- [ ] Update `src/constants/api_endpoints.py`.

## 🛡️ Verification
- [ ] **Test**: Backend responds with Snap Token.
- [ ] **Test**: UI renders Payment Popup / Code.
- [ ] **Audit**: No Server Key in Client Code.

## ✅ Finalization
- [ ] Update `CHANGELOG.md`.
- [ ] Mark Checklist as **APPLIED**.
