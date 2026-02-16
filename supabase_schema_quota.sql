-- ADVANCED AI QUOTA SYSTEM
-- Supports Tier-based limits + Admin Overrides

-- 1. Subscription Tier (Package Level)
alter table public.user_profiles 
add column if not exists subscription_tier text default 'STANDARD';

-- 2. Manual Override (User Level)
-- If set (not null), this overrides the Tier Limit. 
-- Useful for punishing abuse (set to 0) or giving extra bonus (set to 1000).
alter table public.user_profiles 
add column if not exists ai_limit_override int default null;

-- 3. Lifetime Analytics
alter table public.user_profiles 
add column if not exists ai_total_requests bigint default 0;

-- 4. Index for Admin Dashboard performance
create index if not exists idx_profiles_hwid on public.user_profiles(hwid);
