-- GRAVITY MARKETPLACE SCHEMA (Finance Core)
-- Author: Haineo AI
-- Date: 28 Jan 2026

-- 1. MARKETPLACE PRESETS (Barang Dagangan)
create table if not exists public.marketplace_presets (
  id uuid default gen_random_uuid() primary key,
  seller_id text not null references public.user_profiles(hwid),
  title text not null,
  description text,
  price_idr bigint not null default 0,
  price_usd decimal(10,2) not null default 0,
  config_json jsonb not null, -- The Strategy Logic
  
  -- PROOF OF PROFIT METRICS (Verified by Telemetry)
  verified_win_rate decimal(5,2) default 0,
  verified_profit_factor decimal(5,2) default 0,
  verified_days_tested int default 0,
  is_verified boolean default false,
  
  sales_count int default 0,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- 2. USER WALLETS (Dompet Digital Manager)
create table if not exists public.user_wallets (
  user_id text primary key references public.user_profiles(hwid),
  balance_active decimal(12,2) default 0, -- Ready to Withdraw
  balance_pending decimal(12,2) default 0, -- Escrow (3 days hold)
  total_earned decimal(12,2) default 0,
  updated_at timestamptz default now()
);

-- 3. MARKETPLACE ORDERS (Transaksi)
create table if not exists public.marketplace_orders (
  order_id text primary key, -- Midtrans Order ID (e.g., ORD-12345)
  buyer_id text not null references public.user_profiles(hwid),
  preset_id uuid references public.marketplace_presets(id),
  
  amount_gross decimal(12,2) not null,
  platform_fee decimal(12,2) not null, -- 10-20% cut
  amount_net decimal(12,2) not null, -- Goes to Seller
  
  status text default 'PENDING', -- PENDING, PAID, FAILED, REFUNDED
  payment_method text, -- 'gopay', 'bank_transfer', etc.
  snap_token text,
  
  created_at timestamptz default now(),
  paid_at timestamptz
);

-- 4. PAYOUT REQUESTS (Pencairan Dana)
create table if not exists public.payout_requests (
  id uuid default gen_random_uuid() primary key,
  user_id text not null references public.user_profiles(hwid),
  amount decimal(12,2) not null,
  bank_name text not null,
  bank_number text not null,
  account_holder text not null,
  
  status text default 'REQUESTED', -- REQUESTED, APPROVED, REJECTED
  admin_note text,
  proof_attachment text,
  
  created_at timestamptz default now()
);

-- RLS POLICIES (Zero Trust Draft)
alter table public.marketplace_presets enable row level security;
alter table public.marketplace_orders enable row level security;
alter table public.user_wallets enable row level security;
alter table public.payout_requests enable row level security;

-- (Policies need to be applied in Supabase Dashboard or separate migration)
