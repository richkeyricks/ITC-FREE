-- 🛒 MARKETPLACE ORDERS (Transaction Ledger)
-- 🎯 ROLE: Central Record of all Transactions (Pending, Success, Failed)
-- 🔗 LINK: midtrans_webhook -> updates this table

create table if not exists public.marketplace_orders (
  id uuid default gen_random_uuid() primary key,
  order_id text not null unique, -- "ORDER-UUID" from PaymentService
  user_id text not null references public.user_profiles(hwid),
  
  -- Item Details
  preset_id text not null, -- Reference to preset/item
  preset_name text, -- Snapshot of name
  amount decimal(12,2) not null,
  
  -- Payment Status
  status text default 'PENDING', -- PENDING, SUCCESS, FAILED, CHALLENGE
  payment_type text, -- credit_card, gopay, bank_transfer
  fraud_status text, -- accept, deny, challenge
  
  -- Midtrans Metadata
  snap_token text,
  redirect_url text,
  
  -- Timestamps
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  paid_at timestamptz
);

-- RLS: Users can only see their own orders
alter table public.marketplace_orders enable row level security;
create policy "Users see own orders" on public.marketplace_orders
  for select using (auth.uid()::text = user_id);

-- INDEX for fast lookups by Order ID (Critical for Webhook)
create index if not exists idx_orders_order_id on public.marketplace_orders(order_id);
