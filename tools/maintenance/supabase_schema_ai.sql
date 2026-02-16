-- Create AI Usage Tracking Table (Daily Aggregation)
create table if not exists public.ai_usage_daily (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references auth.users(id) on delete cascade not null,
  usage_date date default current_date not null,
  request_count int default 1,
  last_request_at timestamptz default now(),
  
  -- Prevent multiple rows for same user+date
  unique(user_id, usage_date)
);

-- Enable RLS
alter table public.ai_usage_daily enable row level security;

-- Policies
-- Users can view their own usage
create policy "Users view own AI usage"
on public.ai_usage_daily for select
using (auth.uid() = user_id);

-- Admin View Policy (assuming specific admin email or role, simplified here)
-- Ideally handled via Supabase Service Role or separate Admin Table logic

-- Function to Increment Usage (Atomic Update)
create or replace function increment_ai_usage(p_user_id uuid)
returns void as $$
begin
  insert into public.ai_usage_daily (user_id, usage_date, request_count)
  values (p_user_id, current_date, 1)
  on conflict (user_id, usage_date)
  do update set 
    request_count = ai_usage_daily.request_count + 1,
    last_request_at = now();
end;
$$ language plpgsql security definer;
