-- ══════════════════════════════════════════════════════════════════════════════
-- 🚀 QUANTUM SIGNAL MARKETPLACE: DATABASE INITIALIZATION
-- 🛡️ Applied to: Supabase SQL Editor
-- ══════════════════════════════════════════════════════════════════════════════

-- 1. Create Signal Marketplace Table
-- Stores all active and historic signal registrations
CREATE TABLE IF NOT EXISTS marketplace_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    seller_id TEXT REFERENCES user_profiles(hwid) ON DELETE CASCADE,
    title TEXT NOT NULL,
    channel_id TEXT NOT NULL,
    price_idr FLOAT DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    listing_fee_paid BOOLEAN DEFAULT true, -- Logic: Fee already deducted in Python layer
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metrics_json JSONB DEFAULT '{}'::jsonb
);

-- 2. Security: Row Level Security (RLS)
ALTER TABLE marketplace_signals ENABLE ROW LEVEL SECURITY;

-- 3. Policy: Public Visibility
-- Allows any authenticated user to browse available signals
CREATE POLICY "Public: View Active Signals" ON marketplace_signals
    FOR SELECT USING (is_active = true);

-- 4. Policy: Provider Control
-- Signal Providers can manage their own listings
-- Linkage is via HWID (seller_id)
CREATE POLICY "Provider: Manage Own Signals" ON marketplace_signals
    FOR ALL USING (seller_id = (SELECT hwid FROM user_profiles WHERE id = auth.uid() LIMIT 1));

-- 5. Audit View (Optional for Admin)
-- View all fee transactions (if needed for debugging)
-- SELECT * FROM marketplace_signals ORDER BY created_at DESC;

-- ══════════════════════════════════════════════════════════════════════════════
-- ✅ DEPLOYMENT COMPLETE: Signal Marketplace is now active.
-- ══════════════════════════════════════════════════════════════════════════════
