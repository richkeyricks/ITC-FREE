# CHECKLIST: Affiliate 2.0 (Viral Engine) 🦠

## 1. Database & Schema
- [ ] **Run Migration:** Execute `src/supabase_schema_affiliate.sql` in Supabase SQL Editor.
- [ ] **RLS Policies:** Verify policies allow public code lookup but private commission viewing.

## 2. Logic Layer (`affiliate_service.py`)
- [ ] **Code Generator:** Implement `generate_affiliate_code(user_id)` (Random 6-char alphanumeric or Custom).
- [ ] **Registration:** Implement `register_referral(new_user_id, code)`.
- [ ] **Commission Trigger:** Implement `process_commission(order_id)` that runs AFTER a successful payment.
    - [ ] Calculate 10% of `net_amount`.
    - [ ] Update `affiliate_commissions` table.
    - [ ] Update Referrer's `user_wallets` (Pending Balance).

## 3. UI Layer
- [ ] **Merchant Dashboard Update:**
    - [ ] Add "Affiliate Program" Tab or Card.
    - [ ] Display "My Referral Link" (e.g., `gravity.id/ref/RICK01`).
    - [ ] Show "Total Referred Users" and "Total Commission".
- [ ] **Signup Integration (Optional for MVP):**
    - [ ] Add "Referral Code (Optional)" field in Login/Signup screen? (Or just link heavy).

## 4. Testing
- [ ] **Unit Test:** Generate code -> Check Uniqueness.
- [ ] **Flow Test:** User A invites User B -> User B buys -> User A gets money.
