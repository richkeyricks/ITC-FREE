-- GRAVITY AFFILIATE SCHEMA (Viral Engine)
-- Author: Haineo AI
-- Date: 28 Jan 2026

-- 1. AFFILIATE CODES (Public Identity)
-- Maps a User to their unique referral code (e.g. "RICK01")
create table if not exists public.affiliate_codes (
  code text primary key, -- The Referral Code (Unique)
  user_id text not null unique references public.user_profiles(hwid),
  created_at timestamptz default now()
);

-- 2. REFERRAL TRACKING (The Network)
-- Links a new user to their referrer
create table if not exists public.affiliate_referrals (
  id uuid default gen_random_uuid() primary key,
  referrer_id text not null references public.user_profiles(hwid), -- Who invited
  referee_id text not null unique references public.user_profiles(hwid), -- Who joined (One parent only)
  
  status text default 'ACTIVE', -- ACTIVE, BANNED
  joined_at timestamptz default now()
);

-- 3. COMMISSIONS LEDGER (The Money)
-- Tracks every earning event
create table if not exists public.affiliate_commissions (
  id uuid default gen_random_uuid() primary key,
  referrer_id text not null references public.user_profiles(hwid),
  
  source_order_id text references public.marketplace_orders(order_id), -- Linked to a sale
  amount_commission decimal(12,2) not null, -- The 10% cut
  
  base_amount decimal(12,2) not null, -- The original sale amount
  commission_rate decimal(5,2) default 10.0, -- Snapshot of rate at time of sale
  
  status text default 'PENDING', -- PENDING (Wait for money back guarantee), CLEARED, PAID
  created_at timestamptz default now()
);

-- RLS POLICIES
alter table public.affiliate_codes enable row level security;
alter table public.affiliate_referrals enable row level security;
alter table public.affiliate_commissions enable row level security;

-- Policy: Public Read for Codes (To verify validity)
create policy "Public Read Codes" on public.affiliate_codes for select using (true);
-- Policy: User can create their own code
create policy "User Create Code" on public.affiliate_codes for insert with check (auth.uid()::text = user_id);

-- Policy: Referrals (Referrer can see who they invited)
create policy "Referrer See Downline" on public.affiliate_referrals for select using (referrer_id = auth.uid()::text);

-- Policy: Commissions (Only Owner)
create policy "Owner See Commissions" on public.affiliate_commissions for select using (referrer_id = auth.uid()::text);
