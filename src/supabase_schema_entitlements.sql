-- 💳 GENESIS PAYMENT PROTOCOL: ENTITLEMENTS TABLE
-- 🎯 ROLE: Single Source of Truth for Paid Access (Web & App)

-- 1. Create the Table
CREATE TABLE IF NOT EXISTS public.entitlements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL,
    tier TEXT NOT NULL CHECK (tier IN ('STANDARD', 'GOLD', 'PLATINUM', 'INSTITUTIONAL')),
    source TEXT DEFAULT 'WEB_PURCHASE', -- 'WEB_PURCHASE', 'IN_APP_PURCHASE', 'MANUAL_GRANT'
    payment_processor_id TEXT, -- Stripe Customer ID / Midtrans ID
    valid_until TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraint: One active entitlement per email per tier? 
    -- Actually, simpler: One email -> One Highest Tier. 
    -- But for now let's just ensure email+tier uniqueness to prevent duplicates.
    UNIQUE(email, tier)
);

-- 2. Enable RLS
ALTER TABLE public.entitlements ENABLE ROW LEVEL SECURITY;

-- 3. Policies

-- Policy A: Users can READ their own entitlement (based on Auth Email)
CREATE POLICY "Users can view own entitlement" ON public.entitlements
    FOR SELECT
    USING (auth.email() = email);

-- Policy B: Service Role (Edge Functions) can FULL CONTROL
-- (Implicit in Supabase, but good to know)

-- Policy C: Public Read? NO. Strictly private.

-- 4. Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_entitlements_email ON public.entitlements(email);
CREATE INDEX IF NOT EXISTS idx_entitlements_tier ON public.entitlements(tier);

-- 5. Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_entitlements_updated_at
    BEFORE UPDATE ON public.entitlements
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();
